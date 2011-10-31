import urlparse
import urllib2
import urllib
import mbxml
import re
import threading
import time
import logging
import httplib
import xml.etree.ElementTree as etree

try:
    # Python >= 2.4
    set, frozenset
except NameError:
    # Python 2.3
    from sets import Set as set, ImmutableSet as frozenset

_useragent = "pythonmusicbrainzngs-0.1"
_log = logging.getLogger("python-musicbrainz-ngs")


# Constants for validation.

class _Entity:
    """Baseclass for querying musicbrainz"""

    _auth_required = False # is authentication required for reading this?

    BROWSE_MUTALS = frozenset()

    @classmethod
    def get_by_id(klass, id, includes=[], release_status=[], release_type=[]):
        params = _check_filter_and_make_params(includes, release_status,
                                               release_type)
        return _do_mb_query(klass, id, includes, params)


    @staticmethod
    def _browse(klass, includes, **params):
        _check_includes_impl(includes, klass.VALID_BROWSE_INCLUDES)
        # remove empty parameters
        for name in params.keys():
            if not params[name]:
                del params[name]
        if len(set(params) & klass.BROWSE_MUTALS) > 1:
            mutals = list(klass.BROWSE_MUTALS)
            mutals.sort()        
            raise Exception("Can't have more than one of %s."
                            % ', '.join(mutals))
        return _do_mb_query(klass, "", includes, params)


class Tag(_Entity): _entity_name = 'tag'
class Rating(_Entity): _entity_name = 'rating'
class Collection(_Entity): _entity_name = 'collection'

class Artist(_Entity):
    _entity_name = 'artist'
    VALID_INCLUDES = frozenset([
        "recordings", "releases", "release-groups", "works", # Subqueries
        "various-artists", "discids", "media",
        "aliases", "tags", "user-tags", "ratings", "user-ratings", # misc
        "artist-rels", "label-rels", "recording-rels", "release-rels",
        "release-group-rels", "url-rels", "work-rels"
        ])
    VALID_SEARCH_FIELDS = frozenset([
        'arid', 'artist', 'sortname', 'type', 'begin', 'end', 'comment',
        'alias', 'country', 'gender', 'tag'
        ])

    VALID_BROWSE_INCLUDES = frozenset([
        "aliases", "tags", "ratings", "user-tags", "user-ratings"])
    BROWSE_MUTALS = frozenset(['recording', 'release', 'release_group']) # work

    @classmethod
    def browse(klass,
               recording=None, release=None, release_group=None,
               includes=[], limit=None, offset=None):
        return _Entity._browse(klass,
                               includes=includes, limit=limit, offset=offset,
                               recording=recording, release=release,
                               release_group=release_group)


class Label(_Entity):
    _entity_name = 'label'
    VALID_INCLUDES = frozenset([
        "releases", # Subqueries
        "discids", "media",
        "aliases", "tags", "user-tags", "ratings", "user-ratings", # misc
        "artist-rels", "label-rels", "recording-rels", "release-rels",
        "release-group-rels", "url-rels", "work-rels"
        ])
    VALID_SEARCH_FIELDS = frozenset([
        'laid', 'label', 'sortname', 'type', 'code', 'country', 'begin',
        'end', 'comment', 'alias', 'tag'
        ])

    VALID_BROWSE_INCLUDES = frozenset([
        "aliases", "tags", "ratings", "user-tags", "user-ratings"])

    @classmethod
    def browse(klass, release=None, includes=[], limit=None, offset=None):
        return _Entity._browse(klass,
                               includes=includes, limit=limit, offset=offset,
                               release=release)


class Recording(_Entity):
    _entity_name = 'recording'
    VALID_INCLUDES = frozenset([
        "artists", "releases", # Subqueries
        "discids", "media", "artist-credits",
        "tags", "user-tags", "ratings", "user-ratings", # misc
        "artist-rels", "label-rels", "recording-rels", "release-rels",
        "release-group-rels", "url-rels", "work-rels"
        ])
    VALID_SEARCH_FIELDS = frozenset([
        'rid', 'recording', 'isrc', 'arid', 'artist', 'artistname',
        'creditname', 'reid', 'release', 'type', 'status', 'tracks',
        'tracksrelease', 'dur', 'qdur', 'tnum', 'position', 'tag'
        ])

    VALID_BROWSE_INCLUDES = frozenset([
        "artist-credits", "tags", "ratings", "user-tags", "user-ratings"])
    BROWSE_MUTALS = frozenset(['artist', 'release'])

    @classmethod
    def browse(klass, artist=None, release=None,
               includes=[], limit=None, offset=None):
        return _Entity._browse(klass,
                               includes=includes, limit=limit, offset=offset,
                               artist=artist, release=release)

class Release(_Entity):
    _entity_name = 'release'
    VALID_INCLUDES = frozenset([
        "artists", "labels", "recordings", "release-groups", "media",
        "artist-credits", "discids", "puids", "echoprints", "isrcs",
        "artist-rels", "label-rels", "recording-rels", "release-rels",
        "release-group-rels", "url-rels", "work-rels", "recording-level-rels",
        "work-level-rels"
        ])
    VALID_SEARCH_FIELDS = frozenset([
        'reid', 'release', 'arid', 'artist', 'artistname', 'creditname',
        'type', 'status', 'tracks', 'tracksmedium', 'discids',
        'discidsmedium', 'mediums', 'date', 'asin', 'lang', 'script',
        'country', 'date', 'label', 'catno', 'barcode', 'puid'
        ])
    VALID_BROWSE_INCLUDES = frozenset([
        "artist-credits", "labels", "recordings"])
    BROWSE_MUTALS = frozenset(['artist', 'label',' recording', 'release_group'])
    VALID_TYPES = frozenset([
        "nat", "album", "single", "ep", "compilation", "soundtrack", "spokenword",
        "interview", "audiobook", "live", "remix", "other"
        ])
    VALID_STATI = frozenset([
            "official", "promotion", "bootleg", "pseudo-release"])

    @classmethod
    def browse(klass,
               artist=None, label=None, recording=None, release_group=None,
               release_status=[], release_type=[],
               includes=[], limit=None, offset=None):
        # track_artist param doesn't work yet
        if not release_status and not release_type:
            raise InvalidFilterError("Need at least one release status or type")
        filter = _check_filter_and_make_params("releases",
                                               release_status, release_type)
        return _Entity._browse(klass,
                               includes=includes, limit=limit, offset=offset,
                               artist=artist, label=label, 
                               recording=recording, release_group=release_group,
                               **filter)

class ReleaseGroup(_Entity):
    _entity_name = 'release-group'
    VALID_INCLUDES = frozenset([
        "artists", "releases", "discids", "media",
        "artist-credits", "tags", "user-tags", "ratings", "user-ratings", # misc
        "artist-rels", "label-rels", "recording-rels", "release-rels",
        "release-group-rels", "url-rels", "work-rels"
        ])
    VALID_SEARCH_FIELDS = frozenset([
        'rgid', 'releasegroup', 'reid', 'release', 'arid', 'artist',
        'artistname', 'creditname', 'type', 'tag'
        ])
    VALID_BROWSE_INCLUDES = frozenset([
        "artist-credits", "tags", "ratings", "user-tags", "user-ratings"])
    BROWSE_MUTALS = frozenset(['artist', 'release'])

    @classmethod
    def browse(klass,
               artist=None, release=None, release_type=[],
               includes=[], limit=None, offset=None):
        if not release_type:
            raise InvalidFilterError("Need at least one release type")
        filter = _check_filter_and_make_params("release-groups", [], release_type)
        return _Entity._browse(klass,
                               includes=includes, limit=limit, offset=offset,
                               artist=artist, release=release,
                               release_type=release_type, **filter)

class Work(_Entity):
    _entity_name = 'work'
    VALID_INCLUDES = frozenset([
        "artists", # Subqueries
        "aliases", "tags", "user-tags", "ratings", "user-ratings", # misc
        "artist-rels", "label-rels", "recording-rels", "release-rels",
        "release-group-rels", "url-rels", "work-rels"
        ])
    VALID_SEARCH_FIELDS = frozenset([
        'wid', 'work', 'iswc', 'type', 'arid', 'artist', 'alias', 'tag'
        ])

    def get_by_id(klass, id, includes=[]):
        return _do_mb_query(klass, id, includes)


class DiscId(_Entity):
    _entity_name = 'discid'
    VALID_INCLUDES = frozenset([
        "artists", "labels", "recordings", "release-groups", "puids",
        "echoprints", "isrcs"
        ])

class EchoPrint(_Entity):
    _entity_name = 'echprint'
    VALID_INCLUDES = frozenset(["artists", "releases"])


class PUID(_Entity):
    _entity_name = 'puid'
    VALID_INCLUDES = frozenset(
        ["artists", "releases", "puids", "echoprints", "isrcs"])


class ISRC(_Entity):
    _entity_name = 'isrc'
    VALID_INCLUDES = frozenset(
        ["artists", "releases", "puids", "echoprints", "isrcs"])

class ISWC(_Entity):
    _entity_name = 'iswc'
    VALID_INCLUDES = frozenset(["artists"])

class Collection(_Entity): _entity_name = 'collection'


# Exceptions.

class MusicBrainzError(Exception):
    """Base class for all exceptions related to MusicBrainz."""
    pass

class UsageError(MusicBrainzError):
    """Error related to misuse of the module API."""
    pass

class InvalidSearchFieldError(UsageError):
    pass

class InvalidIncludeError(UsageError):
    def __init__(self, msg='Invalid Includes', reason=None):
        super(InvalidIncludeError, self).__init__(self)
        self.msg = msg
        self.reason = reason

    def __str__(self):
        return self.msg

class InvalidFilterError(UsageError):
    def __init__(self, msg='Invalid Includes', reason=None):
        super(InvalidFilterError, self).__init__(self)
        self.msg = msg
        self.reason = reason

    def __str__(self):
        return self.msg

class WebServiceError(MusicBrainzError):
    """Error related to MusicBrainz API requests."""
    def __init__(self, message=None, cause=None):
        """Pass ``cause`` if this exception was caused by another
        exception.
        """
        self.message = message
        self.cause = cause
    
    def __str__(self):
        if self.message:
            msg = "%s, " % self.message
        else:
            msg = ""
        msg += "caused by: %s" % str(self.cause)
        return msg

class NetworkError(WebServiceError):
    """Problem communicating with the MB server."""
    pass

class ResponseError(WebServiceError):
    """Bad response sent by the MB server."""
    pass


# Helpers for validating and formatting allowed sets.

def _check_includes_impl(includes, valid_includes):
    assert isinstance(valid_includes, frozenset)
    invalid = set(includes) - valid_includes
    if invalid:
        raise InvalidIncludeError("Bad includes",
                  "%s is not a valid include" % invalid.pop())

def _check_includes(entity, inc):
    _check_includes_impl(inc, entity.VALID_INCLUDES)

def _check_filter(values, valid):
    assert isinstance(valid, frozenset)
    invalid = set(values) - valid
    if invalid:
        raise InvalidFilterError(invalid.pop())

def _check_filter_and_make_params(includes, release_status=[], release_type=[]):
    """Check that the status or type values are valid. Then, check that
    the filters can be used with the given includes. Return a params
    dict that can be passed to _do_mb_query.
    """
    if isinstance(release_status, basestring):
        release_status = [release_status]
    if isinstance(release_type, basestring):
        release_type = [release_type]
    _check_filter(release_status, Release.VALID_STATI)
    _check_filter(release_type, Release.VALID_TYPES)

    if release_status and "releases" not in includes:
        raise InvalidFilterError("Can't have a status with no release include")
    if release_type and ("release-groups" not in includes and
                         "releases" not in includes):
        raise InvalidFilterError("Can't have a release type with no "
                                 "release-group include")

    # Build parameters.
    params = {}
    if len(release_status):
        params["status"] = "|".join(release_status)
    if len(release_type):
        params["type"] = "|".join(release_type)
    return params


# Global authentication and endpoint details.

user = password = ""
hostname = "musicbrainz.org"
_client = ""

def auth(u, p):
    """Set the username and password to be used in subsequent queries to
    the MusicBrainz XML API that require authentication.
    """
    global user, password
    user = u
    password = p

def set_client(c):
    """ Set the client to be used in requests. This must be set before any
    data submissions are made.
    """
    global _client
    _client = c


# Rate limiting.

limit_interval = 1.0
limit_requests = 1

def set_rate_limit(new_interval=1.0, new_requests=1):
    """Sets the rate limiting behavior of the module. Must be invoked
    before the first Web service call.  Specify the number of requests
    (`new_requests`) that may be made per given interval
    (`new_interval`).
    """
    global limit_interval
    global limit_requests
    limit_interval = new_interval
    limit_requests = new_requests

class _rate_limit(object):
    """A decorator that limits the rate at which the function may be
    called. The rate is controlled by the `limit_interval` and
    `limit_requests` global variables.  The limiting is thread-safe;
    only one thread may be in the function at a time (acts like a
    monitor in this sense). The globals must be set before the first
    call to the limited function.
    """
    def __init__(self, fun):
        self.fun = fun
        self.last_call = 0.0
        self.lock = threading.Lock()
        self.remaining_requests = None # Set on first invocation.

    def _update_remaining(self):
        """Update remaining requests based on the elapsed time since
        they were last calculated.
        """
        # On first invocation, we have the maximum number of requests
        # available.
        if self.remaining_requests is None:
            self.remaining_requests = float(limit_requests)

        else:
            since_last_call = time.time() - self.last_call
            self.remaining_requests += since_last_call * \
                                       (limit_requests / limit_interval)
            self.remaining_requests = min(self.remaining_requests,
                                          float(limit_requests))

        self.last_call = time.time()

    def __call__(self, *args, **kwargs):
        with self.lock:
            self._update_remaining()

            # Delay if necessary.
            while self.remaining_requests < 0.999:
                time.sleep((1.0 - self.remaining_requests) *
                           (limit_requests / limit_interval))
                self._update_remaining()

            # Call the original function, "paying" for this call.
            self.remaining_requests -= 1.0
            return self.fun(*args, **kwargs)


# Generic support for making HTTP requests.

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

class _DigestAuthHandler(urllib2.HTTPDigestAuthHandler):
    def get_authorization (self, req, chal):
        qop = chal.get ('qop', None)
        if qop and ',' in qop and 'auth' in qop.split (','):
            chal['qop'] = 'auth'

        return urllib2.HTTPDigestAuthHandler.get_authorization (self, req, chal)

class _MusicbrainzHttpRequest(urllib2.Request):
    """ A custom request handler that allows DELETE and PUT"""
    def __init__(self, method, url, data=None):
        urllib2.Request.__init__(self, url, data)
        allowed_m = frozenset(["GET", "POST", "DELETE", "PUT"])
        if method not in allowed_m:
            raise ValueError("invalid method: %s" % method)
        self.method = method

    def get_method(self):
        return self.method


# Core (internal) functions for calling the MB API.

def _safe_open(opener, req, body=None, max_retries=8, retry_delay_delta=2.0):
    """Open an HTTP request with a given URL opener and (optionally) a
    request body. Transient errors lead to retries.  Permanent errors
    and repeated errors are translated into a small set of handleable
    exceptions. Returns a file-like object.
    """
    last_exc = None
    for retry_num in range(max_retries):
        if retry_num: # Not the first try: delay an increasing amount.
            _log.debug("retrying after delay (#%i)" % retry_num)
            time.sleep(retry_num * retry_delay_delta)

        try:
            if body:
                f = opener.open(req, body)
            else:
                f = opener.open(req)

        except urllib2.HTTPError, exc:
            if exc.code in (400, 404):
                # Bad request, not found, etc.
                raise ResponseError(cause=exc)
            elif exc.code in (503, 502, 500):
                # Rate limiting, internal overloading...
                _log.debug("HTTP error %i" % exc.code)
            else:
                # Other, unknown error. Should handle more cases, but
                # retrying for now.
                _log.debug("unknown HTTP error %i" % exc.code)
            last_exc = exc
        except httplib.BadStatusLine, exc:
            _log.debug("bad status line")
            last_exc = exc
        except httplib.HTTPException, exc:
            _log.debug("miscellaneous HTTP exception: %s" % str(exc))
            last_exc = exc
        except urllib2.URLError, exc:
            raise NetworkError(cause=exc)
        except IOError, exc:
            raise NetworkError(cause=exc)
        else:
            # No exception! Yay!
            return f
    
    # Out of retries!
    raise NetworkError("retried %i times" % max_retries, last_exc)

@_rate_limit
def _mb_request(path, method='GET', auth_required=False, client_required=False,
                args=None, data=None, body=None):
    """Makes a request for the specified `path` (endpoint) on /ws/2 on
    the globally-specified hostname. Parses the responses and returns
    the resulting object.  `auth_required` and `client_required` control
    whether exceptions should be raised if the client and
    username/password are left unspecified, respectively.
    """
    args = dict(args) or {}

    # Add client if required.
    if client_required and _client == "":
        raise UsageError("set a client name with "
                         "musicbrainz.set_client(\"client-version\")")
    elif client_required:
        args["client"] = _client

    # Construct the full URL for the request, including hostname and
    # query string.
    url = urlparse.urlunparse((
        'http',
        hostname,
        '/ws/2/%s' % path,
        '',
        urllib.urlencode(args),
        ''
    ))
    _log.debug("%s request for %s" % (method, url))
    
    # Set up HTTP request handler and URL opener.
    httpHandler = urllib2.HTTPHandler(debuglevel=0)
    handlers = [httpHandler]
    opener = urllib2.build_opener(*handlers)

    # Add credentials if required.
    if auth_required:
        if not user:
            raise UsageError("authorization required; "
                             "use musicbrainz.auth(u, p) first")
        passwordMgr = _RedirectPasswordMgr()
        authHandler = _DigestAuthHandler(passwordMgr)
        authHandler.add_password("musicbrainz.org", (), user, password)
        handlers.append(authHandler)
    
    # Make request.
    req = _MusicbrainzHttpRequest(method, url, data)
    req.add_header('User-Agent', _useragent)
    if body:
        req.add_header('Content-Type', 'application/xml; charset=UTF-8')
    f = _safe_open(opener, req, body)

    # Parse the response.
    try:
        return mbxml.parse_message(f)
    except etree.ParseError, exc:
        raise ResponseError(cause=exc)
    except UnicodeError, exc:
        raise ResponseError(cause=exc)

def _is_auth_required(entity, includes):
    """ Some calls require authentication. This returns
    True if a call does, False otherwise
    """
    if hasattr(entity, '_auth_required'):
        return entity._auth_required
    elif "user-tags" in includes or "user-ratings" in includes:
        return True
    elif entity.startswith("collection"):
        return True
    else:
        return False

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
    auth_required = _is_auth_required(entity, includes)
    args = dict(params)
    if len(includes) > 0:
        inc = " ".join(includes)
        args["inc"] = inc

    # Build the endpoint components.
    path = '%s/%s' % (entity._entity_name, id)
    return _mb_request(path, 'GET', auth_required, args=args)

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
        if key not in entity.VALID_SEARCH_FIELDS:
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

def _do_mb_delete(path):
    """Send a DELETE request for the specified object.
    """
    return _mb_request(path, 'DELETE', True, True)

def _do_mb_put(path):
    """Send a PUT request for the specified object.
    """
    return _mb_request(path, 'PUT', True, True)

def _do_mb_post(path, body):
    """Perform a single POST call for an endpoint with a specified
    request body.
    """
    return _mb_request(path, 'PUT', True, True, body=body)


# The main interface!


# Single entity by ID
get_artist_by_id = Artist.get_by_id
get_label_by_id = Label.get_by_id
get_recording_by_id = Recording.get_by_id
get_release_by_id = Release.get_by_id
get_release_group_by_id = ReleaseGroup.get_by_id
get_work_by_id = Work.get_by_id

# Searching

def artist_search(query='', limit=None, offset=None, **fields):
    """Search for artists by a free-form `query` string and/or any of
    the following keyword arguments specifying field queries:
    arid, artist, sortname, type, begin, end, comment, alias, country,
    gender, tag
    """
    return _do_mb_search(Artist, query, fields, limit, offset)

def label_search(query='', limit=None, offset=None, **fields):
    """Search for labels by a free-form `query` string and/or any of
    the following keyword arguments specifying field queries:
    laid, label, sortname, type, code, country, begin, end, comment,
    alias, tag
    """
    return _do_mb_search(Label, query, fields, limit, offset)

def recording_search(query='', limit=None, offset=None, **fields):
    """Search for recordings by a free-form `query` string and/or any of
    the following keyword arguments specifying field queries:
    rid, recording, isrc, arid, artist, artistname, creditname, reid,
    release, type, status, tracks, tracksrelease, dur, qdur, tnum,
    position, tag
    """
    return _do_mb_search(Recording, query, fields, limit, offset)

def release_search(query='', limit=None, offset=None, **fields):
    """Search for releases by a free-form `query` string and/or any of
    the following keyword arguments specifying field queries:
    reid, release, arid, artist, artistname, creditname, type, status,
    tracks, tracksmedium, discids, discidsmedium, mediums, date, asin,
    lang, script, country, date, label, catno, barcode, puid
    """
    return _do_mb_search(Release, query, fields, limit, offset)

def release_group_search(query='', limit=None, offset=None, **fields):
    """Search for release groups by a free-form `query` string and/or
    any of the following keyword arguments specifying field queries:
    rgid, releasegroup, reid, release, arid, artist, artistname,
    creditname, type, tag
    """
    return _do_mb_search(ReleaseGroup, query, fields, limit, offset)

def work_search(query='', limit=None, offset=None, **fields):
    """Search for works by a free-form `query` string and/or any of
    the following keyword arguments specifying field queries:
    wid, work, iswc, type, arid, artist, alias, tag
    """
    return _do_mb_search(Work, query, fields, limit, offset)


# Lists of entities
def get_releases_by_discid(id, includes=[], release_type=[]):
    params = _check_filter_and_make_params(includes, release_type=release_type)
    return _do_mb_query(DiscId, id, includes, params)

def get_recordings_by_echoprint(echoprint, includes=[],
                                release_status=[], release_type=[]):
    params = _check_filter_and_make_params(includes,
                                           release_status, release_type)
    return _do_mb_query(EchoPrint, echoprint, includes, params)

def get_recordings_by_puid(puid, includes=[],
                           release_status=[], release_type=[]):
    params = _check_filter_and_make_params(includes,
                                           release_status, release_type)
    return _do_mb_query(PUID, puid, includes, params)

def get_recordings_by_isrc(isrc, includes=[],
                           release_status=[], release_type=[]):
    params = _check_filter_and_make_params(includes,
                                           release_status, release_type)
    return _do_mb_query(ISRC, isrc, includes, params)

def get_works_by_iswc(iswc, includes=[]):
    return _do_mb_query(ISWC, iswc, includes)

# Browse methods
# Browse include are a subset of regular get includes, so we check them here
# and the test in _do_mb_query will pass anyway.
browse_artist = Artist.browse
browse_label = Label.browse
browse_recording = Recording.browse
browse_release = Release.browse
browse_release_group = ReleaseGroup.browse
#browse_work is defined in the docs but has no browse criteria


# Collections
def get_all_collections():
    # Missing <release-list count="n"> the count in the reply
    return _do_mb_query(Collection, '')

def get_releases_in_collection(collection):
    return _do_mb_query(Collection, "%s/releases" % collection)

# Submission methods

def submit_barcodes(barcodes):
    """
    Submits a set of {release1: barcode1, release2:barcode2}
    Must call auth(user, pass) first
    """
    query = mbxml.make_barcode_request(barcodes)
    return _do_mb_post(Release, query)

def submit_puids(puids):
    query = mbxml.make_puid_request(puids)
    return _do_mb_post(Recording, query)

def submit_echoprints(echoprints):
    query = mbxml.make_echoprint_request(echoprints)
    return _do_mb_post(Recording, query)

def submit_isrcs(isrcs):
    raise NotImplementedError

def submit_tags(artist_tags={}, recording_tags={}):
    """ Submit user tags.
        Artist or recording parameters are of the form:
        {'entityid': [taglist]}
    """
    query = mbxml.make_tag_request(artist_tags, recording_tags)
    return _do_mb_post(Tag, query)

def submit_ratings(artist_ratings={}, recording_ratings={}):
    """ Submit user ratings.
        Artist or recording parameters are of the form:
        {'entityid': rating}
    """
    query = mbxml.make_rating_request(artist_ratings, recording_ratings)
    return _do_mb_post(Rating, query)

def add_releases_to_collection(collection, releases=[]):
    # XXX: Maximum URI length of 16kb means we should only allow ~400 releases
    releaselist = ";".join(releases)
    _do_mb_put("collection/%s/releases/%s" % (collection, releaselist))

def remove_releases_from_collection(collection, releases=[]):
    releaselist = ";".join(releases)
    _do_mb_delete("collection/%s/releases/%s" % (collection, releaselist))
