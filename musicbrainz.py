import sys
import urlparse
import urllib2
import urllib
import mbxml

def do_mb_query(entity, id, includes=[]):
	# XXX: Paging
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
	print mbxml.parse_message(f)

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

def get_artist_by_id(id, includes=[]):
	valid_inc = ["recordings", "releases", "release-groups", "works"]
	check_includes(valid_inc, includes)
	do_mb_query("artist", id, includes)

def search_artist(query, includes):
	pass

def browse_artist(filters, includes):
	pass

def get_label_by_id(id, includes=[]):
	valid_inc = ["releases"]
	check_includes(valid_inc, includes)
	do_mb_query("label", id, includes)

def search_label(query, includes):
	pass

def browse_releases(includes, status, typ):
	pass

def browse_release_groups(includes, status, typ):
	pass

def get_recording_by_id(id, includes=[]):
	valid_inc = ["artists", "releases"]
	check_includes(valid_inc, includes)
	do_mb_query("recording", id, includes)

def get_release_by_id(id, includes=[]):
	valid_inc = ["artists", "labels", "recordings", "release-groups"]
	check_includes(valid_inc, includes)
	do_mb_query("release", id, includes)

def get_release_group_by_id(id, includes=[]):
	valid_inc = ["artists", "releases"]
	check_includes(valid_inc, includes)
	do_mb_query("release-group", id, includes)

def get_work_by_id(id, includes=[]):
	valid_inc = ["artists"]
	check_includes(valid_inc, includes)
	do_mb_query("work", id, includes)

###

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

