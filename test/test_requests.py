import unittest
import musicbrainzngs
from musicbrainzngs import musicbrainz
from test import _common


class ArgumentTest(unittest.TestCase):
    """Tests request methods to ensure they're enforcing general parameters
    (useragent, authentication)."""

    def setUp(self):
        self.opener = _common.FakeOpener("<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener.add_handlers_and_return(args)
        musicbrainz.set_rate_limit(False)

    def tearDown(self):
        musicbrainz.set_rate_limit(True)

    def test_no_client(self):
        musicbrainzngs.set_useragent("testapp", "0.1", "test@example.org")
        musicbrainz._mb_request(path="foo", client_required=False)
        self.assertFalse("testapp" in self.opener.myurl)

    def test_client(self):
        musicbrainzngs.set_useragent("testapp", "0.1", "test@example.org")
        musicbrainz._mb_request(path="foo", client_required=True)
        self.assertTrue("testapp" in self.opener.myurl)

    def test_false_useragent(self):
        self.assertRaises(ValueError, musicbrainzngs.set_useragent, "", "0.1",
                "test@example.org")
        self.assertRaises(ValueError, musicbrainzngs.set_useragent, "test", "",
                "test@example.org")

    def test_missing_auth(self):
        musicbrainz.auth("", "")
        musicbrainz._useragent = "test"
        self.assertRaises(musicbrainzngs.UsageError,
                musicbrainz._mb_request, path="foo",
                auth_required=musicbrainz.AUTH_YES)

    def test_missing_useragent(self):
        musicbrainz._useragent = ""
        self.assertRaises(musicbrainzngs.musicbrainz.UsageError,
                musicbrainz._mb_request, path="foo")

    def test_auth_headers(self):
        musicbrainz._useragent = "test"
        musicbrainz.auth("user", "password")
        req = musicbrainz._mb_request(path="foo", auth_required=musicbrainz.AUTH_YES)
        assert(any([isinstance(handler, musicbrainz._DigestAuthHandler) for handler in self.opener.handlers]))

    def test_auth_headers_ifset(self):
        musicbrainz._useragent = "test"
        musicbrainz.auth("user", "password")
        req = musicbrainz._mb_request(path="foo", auth_required=musicbrainz.AUTH_IFSET)
        assert(any([isinstance(handler, musicbrainz._DigestAuthHandler) for handler in self.opener.handlers]))

    def test_auth_headers_ifset_no_user(self):
        musicbrainz._useragent = "test"
        musicbrainz.auth("", "")
        # if no user and password, auth is not set for AUTH_IFSET
        req = musicbrainz._mb_request(path="foo", auth_required=musicbrainz.AUTH_IFSET)
        assert(not any([isinstance(handler, musicbrainz._DigestAuthHandler) for handler in self.opener.handlers]))


class MethodTest(unittest.TestCase):
    """Tests the various _do_mb_* methods to ensure they're setting the
    using the correct HTTP method."""

    def setUp(self):
        self.opener = _common.FakeOpener("<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener

        musicbrainz.auth("user", "password")
        musicbrainz.set_rate_limit(False)

    def tearDown(self):
        musicbrainz.set_rate_limit(False)

    def test_invalid_method(self):
        self.assertRaises(ValueError, musicbrainz._mb_request, path="foo",
                          method="HUG")

    def test_delete(self):
        musicbrainz._do_mb_delete("foo")
        self.assertEqual("DELETE", self.opener.request.get_method())

    def test_put(self):
        musicbrainz._do_mb_put("foo")
        self.assertEqual("PUT", self.opener.request.get_method())

    def test_post(self):
        musicbrainz._do_mb_post("foo", "body")
        self.assertEqual("POST", self.opener.request.get_method())

    def test_get(self):
        musicbrainz._do_mb_query("artist", 1234, [], [])
        self.assertEqual("GET", self.opener.request.get_method())


class HostnameTest(unittest.TestCase):
    """Test that the protocol, hostname, and port are set as expected"""

    def setUp(self):
        self.opener = _common.FakeOpener("<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        musicbrainz.set_rate_limit(False)

    def tearDown(self):
        musicbrainz.set_rate_limit(True)
        musicbrainzngs.set_hostname("musicbrainz.org", use_https=True)

    def test_default_musicbrainz_https(self):
        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b")
        self.assertEqual("https://musicbrainz.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", self.opener.get_url())

    def test_set_http(self):
        musicbrainzngs.set_hostname("beta.musicbrainz.org")

        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b")
        self.assertEqual("http://beta.musicbrainz.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", self.opener.get_url())

    def test_set_https(self):
        musicbrainzngs.set_hostname("mbmirror.org", use_https=True)

        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b")
        self.assertEqual("https://mbmirror.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", self.opener.get_url())

    def test_set_port(self):
        musicbrainzngs.set_hostname("localhost:8000", use_https=False)

        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b")
        self.assertEqual("http://localhost:8000/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", self.opener.get_url())
