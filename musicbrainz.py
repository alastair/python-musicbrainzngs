import sys
import urlparse
import urllib2
import urllib
import mbxml

# To do:
# artist-credits, various-artists
# User ratings, User tags
# Relationships
# Browse methods
# Search methods
#   http://wiki.musicbrainz.org/Next_Generation_Schema/SearchServerXML
# Paging
# Release type, status

user = password = ""

def auth(u, p):
	global user, password
	user = u
	password = p

def do_mb_query(entity, id, includes=[]):
	args = {}
	if len(includes) > 0:
		inc = " ".join(includes)
		args["inc"] = inc
	url = urlparse.urlunparse(('http',
		'test.musicbrainz.org',
		'/ws/2/%s/%s' % (entity, id),
		'',
		urllib.urlencode(args),
		''))
	print url
	f = urllib2.Request(url)
	f.add_header('User-Agent','pythonmusicbrainzngs-0.1')
	try:
		f = urllib2.urlopen(f)
	except urllib2.URLError, e:
		print "error"
		raise
	return mbxml.parse_message(f)

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

class DigestAuthHandler (urllib2.HTTPDigestAuthHandler):
	def get_authorization (self, req, chal):
		qop = chal.get ('qop', None)
		if qop and ',' in qop and 'auth' in qop.split (','):
			chal['qop'] = 'auth'

		return urllib2.HTTPDigestAuthHandler.get_authorization (self, req, chal)

def do_mb_post(entity, body):
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
		'test.musicbrainz.org',
		'/ws/2/%s' % (entity,),
		'',
		urllib.urlencode(args),
		''))
	print url
	f = urllib2.Request(url)
	f.add_header('User-Agent','pythonmusicbrainzngs-0.1')
	f.add_header('Content-Type', 'application/xml; charset=UTF-8')
	try:
		f = opener.open(f, body)
	except urllib2.URLError, e:
		print e.fp.read()
		raise
	print f.read()
	#return mbxml.parse_message(f)

class InvalidIncludeError(Exception):
	def __init__(self, msg='Invalid Includes', reason=None):
		Exception.__init__(self)
		self.msg = msg
		self.reason = reason

	def __str__(self):
		return self.msg

def check_includes(valid_inc, inc):
	for i in inc:
		if i not in valid_inc:
			raise InvalidIncludeError("Bad includes", "%s is not a valid include" % i)

# Single entity by ID

def get_artist_by_id(id, includes=[]):
	valid_inc = ["recordings", "releases", "release-groups", "works", # Subqueries
	             "discids", "media",
	             "aliases", "tags", "user-tags", "ratings", "user-ratings"] # misc arguments
	check_includes(valid_inc, includes)
	return do_mb_query("artist", id, includes)

def get_label_by_id(id, includes=[]):
	valid_inc = ["releases", # Subqueries
	             "discids", "media",
	             "aliases", "tags", "user-tags", "ratings", "user-ratings"] # misc arguments
	check_includes(valid_inc, includes)
	return do_mb_query("label", id, includes)

def get_recording_by_id(id, includes=[]):
	valid_inc = ["artists", "releases", # Subqueries
	             "discids", "media",
	             "tags", "user-tags", "ratings", "user-ratings"] # misc arguments
	check_includes(valid_inc, includes)
	return do_mb_query("recording", id, includes)

def get_release_by_id(id, includes=[]):
	valid_inc = ["artists", "labels", "recordings", "release-groups", "media", "discids", "puids", "isrcs"]
	check_includes(valid_inc, includes)
	return do_mb_query("release", id, includes)

def get_release_group_by_id(id, includes=[]):
	valid_inc = ["artists", "releases", "discids", "media"]
	check_includes(valid_inc, includes)
	return do_mb_query("release-group", id, includes)

def get_work_by_id(id, includes=[]):
	valid_inc = ["artists", # Subqueries
	             "aliases", "tags", "user-tags", "ratings", "user-ratings"] # misc arguments
	check_includes(valid_inc, includes)
	return do_mb_query("work", id, includes)

# Lists of entities

def get_releases_by_discid(id, includes=[]):
	valid_inc = ["artists", "labels", "recordings", "release-groups", "puids", "isrcs"]
	check_includes(valid_inc, includes)
	return do_mb_query("discid", id, includes)

def get_recordings_by_puid(puid, includes=[]):
	valid_inc = ["artists", "releases", "puids", "isrcs"]
	check_includes(valid_inc, includes)
	return do_mb_query("puid", puid, includes)

def get_recordings_by_isrc(isrc, includes=[]):
	valid_inc = ["artists", "releases", "puids", "isrcs"]
	check_includes(valid_inc, includes)
	return do_mb_query("isrc", isrc, includes)

def get_works_by_iswc(iswc, includes=[]):
	valid_inc = ["artists"]
	check_includes(valid_inc, includes)
	return do_mb_query("iswc", iswc, includes)

# Submission methods

def submit_barcodes(barcodes):
	"""
	Submits a set of {release1: barcode1, release2:barcode2}
	Must call auth(user, pass) first
	"""
	query = mbxml.make_barcode_request(barcodes)
	query = '<?xml version="1.0" encoding="UTF-8"?>' + query
	query = query.replace("ns0:", "")
	do_mb_post("release", query)

def submit_puids(puids):
	query = mbxml.make_puid_request(puids)
	query = '<?xml version="1.0" encoding="UTF-8"?>' + query
	query = query.replace("ns0:", "")
	do_mb_post("recording", query)

def submit_isrcs(isrcs):
	raise NotImplementedError

def submit_tags(artist_tags={}, recording_tags={}):
	""" Submit user tags.
	    Artist or recording parameters are of the form:
	    {'entityid': [taglist]}
	"""
	query = mbxml.make_tag_request(artist_tags, recording_tags)
	query = '<?xml version="1.0" encoding="UTF-8"?>' + query
	query = query.replace("ns0:", "")
	do_mb_post("tag", query)

def submit_ratings(artist_ratings={}, recording_ratings={}):
	""" Submit user ratings.
	    Artist or recording parameters are of the form:
	    {'entityid': rating}
	"""
	query = mbxml.make_rating_request(artist_ratings, recording_ratings)
	query = '<?xml version="1.0" encoding="UTF-8"?>' + query
	query = query.replace("ns0:", "")
	print query
	do_mb_post("rating", query)

