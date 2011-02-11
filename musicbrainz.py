import sys
import urlparse
import urllib2
import urllib
import mbxml

# To do:
# Subqueries
# Subquery incs
# Misc incs
# Browse methods
# Search methods
#   http://wiki.musicbrainz.org/Next_Generation_Schema/SearchServerXML
# Paging
# Release type, status

def do_mb_query(entity, id, includes=[]):
	args = {}
	if len(includes) > 1:
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
	f.add_header('User-Agent','pymb3')
	try:
		f = urllib2.urlopen(f)
	except urllib2.URLError, e:
		print "error"
		raise
	return mbxml.parse_message(f)

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
			print i
			raise InvalidIncludeError("Bad includes", "%s is not a valid include" % i)

# Single entity by ID

def get_artist_by_id(id, includes=[]):
	valid_inc = ["recordings", "releases", "release-groups", "works"]
	check_includes(valid_inc, includes)
	return do_mb_query("artist", id, includes)

def get_label_by_id(id, includes=[]):
	valid_inc = ["releases"]
	check_includes(valid_inc, includes)
	return do_mb_query("label", id, includes)

def get_recording_by_id(id, includes=[]):
	valid_inc = ["artists", "releases"]
	check_includes(valid_inc, includes)
	return do_mb_query("recording", id, includes)

def get_release_by_id(id, includes=[]):
	valid_inc = ["artists", "labels", "recordings", "release-groups"]
	check_includes(valid_inc, includes)
	return do_mb_query("release", id, includes)

def get_release_group_by_id(id, includes=[]):
	valid_inc = ["artists", "releases"]
	check_includes(valid_inc, includes)
	return do_mb_query("release-group", id, includes)

def get_work_by_id(id, includes=[]):
	valid_inc = ["artists"]
	check_includes(valid_inc, includes)
	return do_mb_query("work", id, includes)

# Lists of entities

def get_releases_by_discid(id, includes=[]):
	valid_inc = ["artists", "labels", "recordings", "release-groups"]
	check_includes(valid_inc, includes)
	return do_mb_query("discid", id, includes)

def get_recordings_by_puid(puid, includes=[]):
	valid_inc = ["artists", "releases"]
	check_includes(valid_inc, includes)
	return do_mb_query("puid", puid, includes)

def get_recordings_by_isrc(isrc, includes=[]):
	valid_inc = ["artists", "releases"]
	check_includes(valid_inc, includes)
	return do_mb_query("isrc", isrc, includes)

def get_works_by_iswc(iswc, includes=[]):
	valid_inc = ["artists"]
	check_includes(valid_inc, includes)
	return do_mb_query("iswc", iswc, includes)

# Submission methods

def submit_barcode():
	pass

def submit_puid():
	pass

def submit_isrc():
	pass

def submit_tags():
	pass

def submit_rating():
	pass

