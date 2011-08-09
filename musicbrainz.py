import urlparse
import urllib2
import urllib
import mbxml
import re

# To do:
# artist-credits, various-artists
# User ratings, User tags
# Relationships
# Browse methods
# Paging
# Release type, status, date


# Constants for validation.

VALID_INCLUDES = {
	'artist': [
		"recordings", "releases", "release-groups", "works", # Subqueries
		"discids", "media",
		"aliases", "tags", "user-tags", "ratings", "user-ratings" # misc
	], 
	'label': [
		"releases", # Subqueries
	    "discids", "media",
	    "aliases", "tags", "user-tags", "ratings", "user-ratings" # misc
	],
	'recording': [
		"artists", "releases", # Subqueries
	    "discids", "media",
	    "tags", "user-tags", "ratings", "user-ratings" # misc
	],
	'release': [
		"artists", "labels", "recordings", "release-groups", "media",
		"discids", "puids", "echoprints", "isrcs"
	],
	'release-group': ["artists", "releases", "discids", "media"],
	'work': [
		"artists", # Subqueries
	    "aliases", "tags", "user-tags", "ratings", "user-ratings" # misc
	],
	'discid': [
		"artists", "labels", "recordings", "release-groups", "puids",
		"echoprints", "isrcs"
	],
	'echoprint': ["artists", "releases"],
	'puid': ["artists", "releases", "puids", "echoprints", "isrcs"],
	'isrc': ["artists", "releases", "puids", "echoprints", "isrcs"],
	'iswc': ["artists"],
}
VALID_SEARCH_FIELDS = {
	'artist': [
		'arid', 'artist', 'sortname', 'type', 'begin', 'end', 'comment',
		'alias', 'country', 'gender', 'tag'
	],
	'release-group': [
		'rgid', 'releasegroup', 'reid', 'release', 'arid', 'artist',
		'artistname', 'creditname', 'type', 'tag'
	],
	'release': [
		'reid', 'release', 'arid', 'artist', 'artistname', 'creditname',
		'type', 'status', 'tracks', 'tracksmedium', 'discids',
		'discidsmedium', 'mediums', 'date', 'asin', 'lang', 'script',
		'country', 'date', 'label', 'catno', 'barcode', 'puid'
	],
	'recording': [
		'rid', 'recording', 'isrc', 'arid', 'artist', 'artistname',
		'creditname', 'reid', 'release', 'type', 'status', 'tracks',
		'tracksrelease', 'dur', 'qdur', 'tnum', 'position', 'tag'
	],
	'label': [
		'laid', 'label', 'sortname', 'type', 'code', 'country', 'begin',
		'end', 'comment', 'alias', 'tag'
	],
	'work': [
		'wid', 'work', 'iswc', 'type', 'arid', 'artist', 'alias', 'tag'
	],
}

def _check_includes(entity, inc):
	for i in inc:
		if i not in VALID_INCLUDES[entity]:
			raise InvalidIncludeError("Bad includes",
									  "%s is not a valid include" % i)


# Invalid-argument exceptions.

class InvalidSearchFieldError(Exception):
	pass

class InvalidIncludeError(Exception):
	def __init__(self, msg='Invalid Includes', reason=None):
		Exception.__init__(self)
		self.msg = msg
		self.reason = reason

	def __str__(self):
		return self.msg


# Global authentication and endpoint details.

user = password = ""
hostname = "musicbrainz.org"

def auth(u, p):
	"""Set the username and password to be used in subsequent queries to
	the MusicBrainz XML API that require authentication.
	"""
	global user, password
	user = u
	password = p


# Core functions for calling the MB API.

def _do_mb_query(entity, id, includes=[], params={}):
	"""Make a single GET call to the MusicBrainz XML API. `entity` is a
	string indicated the type of object to be retrieved. The id may be
	empty, in which case the query is a search. `includes` is a list
	of strings that must be valid includes for the entity type. `params`
	is a dictionary of additional parameters for the API call. The
	response is parsed and returned.
	"""
	# Build arguments.
	_check_includes(entity, includes)
	args = dict(params)
	if len(includes) > 0:
		inc = " ".join(includes)
		args["inc"] = inc
	
	# Build the endpoint URL.
	url = urlparse.urlunparse(('http',
		hostname,
		'/ws/2/%s/%s' % (entity, id),
		'',
		urllib.urlencode(args),
		''))
	print url

	# Make the request and parse the response.
	f = urllib2.Request(url)
	f.add_header('User-Agent','pythonmusicbrainzngs-0.1')
	try:
		f = urllib2.urlopen(f)
	except urllib2.URLError, e:
		print "error"
		raise
	return mbxml.parse_message(f)

def _do_mb_search(entity, query='', fields={}, limit=None, offset=None):
	"""Perform a full-text search on the MusicBrainz search server.
	`query` is a free-form query string and `fields` is a dictionary
	of key/value query parameters. They keys in `fields` must be valid
	for the given entity type.
	"""
	# Encode the query terms as a Lucene query string.
	query_parts = [query.replace('\x00', '').strip()]
	for key, value in fields.iteritems():
		# Ensure this is a valid search field.
		if key not in VALID_SEARCH_FIELDS[entity]:
			raise InvalidSearchFieldError(
				'%s is not a valid search field for %s' % (key, entity)
			)

		# Escape Lucene's special characters.
		value = re.sub(r'([+\-&|!(){}\[\]\^"~*?:\\])', r'\\\1', value)
		value = value.replace('\x00', '').strip()
		if value:
			query_parts.append(u'%s:(%s)' % (key, value))
	full_query = u' '.join(query_parts).strip()
	if not full_query:
		raise ValueError('at least one query term is required')

	# Additional parameters to the search.
	params = {'query': full_query}
	if limit:
		params['limit'] = str(limit)
	if offset:
		params['offset'] = str(offset)

	return _do_mb_query(entity, '', [], params)

# From pymb2
class _RedirectPasswordMgr(urllib2.HTTPPasswordMgr):
	def __init__(self):
		self._realms = { }

	def find_user_password(self, realm, uri):
		# ignoring the uri parameter intentionally
		try:
			return self._realms[realm]
		except KeyError:
			return (None, None)

	def add_password(self, realm, uri, username, password):
		# ignoring the uri parameter intentionally
		self._realms[realm] = (username, password)

class DigestAuthHandler(urllib2.HTTPDigestAuthHandler):
	def get_authorization (self, req, chal):
		qop = chal.get ('qop', None)
		if qop and ',' in qop and 'auth' in qop.split (','):
			chal['qop'] = 'auth'

		return urllib2.HTTPDigestAuthHandler.get_authorization (self, req, chal)

def _do_mb_post(entity, body):
	"""Perform a single POST call to the MusicBrainz XML API.
	"""
	if user == "":
		raise Exception("use musicbrainz.auth(u, p) first")
	passwordMgr = _RedirectPasswordMgr()
	authHandler = DigestAuthHandler(passwordMgr)
        authHandler.add_password("musicbrainz.org", (), # no host set
                        user, password)
	opener = urllib2.build_opener()
        opener.add_handler(authHandler)

	args = {"client": "pythonmusicbrainzngs-0.1"}
	url = urlparse.urlunparse(('http',
		hostname,
		'/ws/2/%s' % (entity,),
		'',
		urllib.urlencode(args),
		''))
	#print url
	f = urllib2.Request(url)
	f.add_header('User-Agent','pythonmusicbrainzngs-0.1')
	f.add_header('Content-Type', 'application/xml; charset=UTF-8')
	try:
		f = opener.open(f, body)
	except urllib2.URLError, e:
		if e.fp:
			print e.fp.read()
		raise
	#print f.read()
	return mbxml.parse_message(f)


# Single entity by ID

def get_artist_by_id(id, includes=[]):
	return _do_mb_query("artist", id, includes)

def get_label_by_id(id, includes=[]):
	return _do_mb_query("label", id, includes)

def get_recording_by_id(id, includes=[]):
	return _do_mb_query("recording", id, includes)

def get_release_by_id(id, includes=[]):
	return _do_mb_query("release", id, includes)

def get_release_group_by_id(id, includes=[]):
	return _do_mb_query("release-group", id, includes)

def get_work_by_id(id, includes=[]):
	return _do_mb_query("work", id, includes)


# Searching

def artist_search(query='', limit=None, offset=None, **fields):
	"""Search for artists by a free-form `query` string and/or any of
	the following keyword arguments specifying field queries:
	arid, artist, sortname, type, begin, end, comment, alias, country,
	gender, tag
	"""
	return _do_mb_search('artist', query, fields, limit, offset)

def label_search(query='', limit=None, offset=None, **fields):
	"""Search for labels by a free-form `query` string and/or any of
	the following keyword arguments specifying field queries:
	laid, label, sortname, type, code, country, begin, end, comment,
	alias, tag
	"""
	return _do_mb_search('label', query, fields, limit, offset)

def recording_search(query='', limit=None, offset=None, **fields):
	"""Search for recordings by a free-form `query` string and/or any of
	the following keyword arguments specifying field queries:
	rid, recording, isrc, arid, artist, artistname, creditname, reid,
	release, type, status, tracks, tracksrelease, dur, qdur, tnum,
	position, tag
	"""
	return _do_mb_search('recording', query, fields, limit, offset)

def release_search(query='', limit=None, offset=None, **fields):
	"""Search for releases by a free-form `query` string and/or any of
	the following keyword arguments specifying field queries:
	reid, release, arid, artist, artistname, creditname, type, status,
	tracks, tracksmedium, discids, discidsmedium, mediums, date, asin,
	lang, script, country, date, label, catno, barcode, puid
	"""
	return _do_mb_search('release', query, fields, limit, offset)

def release_group_search(query='', limit=None, offset=None, **fields):
	"""Search for release groups by a free-form `query` string and/or
	any of the following keyword arguments specifying field queries:
	rgid, releasegroup, reid, release, arid, artist, artistname,
	creditname, type, tag
	"""
	return _do_mb_search('release-group', query, fields, limit, offset)

def work_search(query='', limit=None, offset=None, **fields):
	"""Search for works by a free-form `query` string and/or any of
	the following keyword arguments specifying field queries:
	wid, work, iswc, type, arid, artist, alias, tag
	"""
	return _do_mb_search('work', query, fields, limit, offset)


# Lists of entities

def get_releases_by_discid(id, includes=[]):
	return _do_mb_query("discid", id, includes)

def get_recordings_by_echoprint(echoprint, includes=[]):
	return _do_mb_query("echoprint", echoprint, includes)

def get_recordings_by_puid(puid, includes=[]):
	return _do_mb_query("puid", puid, includes)

def get_recordings_by_isrc(isrc, includes=[]):
	return _do_mb_query("isrc", isrc, includes)

def get_works_by_iswc(iswc, includes=[]):
	return _do_mb_query("iswc", iswc, includes)


# Submission methods

def submit_barcodes(barcodes):
	"""
	Submits a set of {release1: barcode1, release2:barcode2}
	Must call auth(user, pass) first
	"""
	query = mbxml.make_barcode_request(barcodes)
	return _do_mb_post("release", query)

def submit_puids(puids):
	query = mbxml.make_puid_request(puids)
	return _do_mb_post("recording", query)

def submit_echoprints(echoprints):
	query = mbxml.make_echoprint_request(echoprints)
	return _do_mb_post("recording", query)

def submit_isrcs(isrcs):
	raise NotImplementedError

def submit_tags(artist_tags={}, recording_tags={}):
	""" Submit user tags.
	    Artist or recording parameters are of the form:
	    {'entityid': [taglist]}
	"""
	query = mbxml.make_tag_request(artist_tags, recording_tags)
	return _do_mb_post("tag", query)

def submit_ratings(artist_ratings={}, recording_ratings={}):
	""" Submit user ratings.
	    Artist or recording parameters are of the form:
	    {'entityid': rating}
	"""
	query = mbxml.make_rating_request(artist_ratings, recording_ratings)
	return _do_mb_post("rating", query)

