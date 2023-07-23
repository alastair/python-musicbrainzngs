import musicbrainzngs
from musicbrainzngs import musicbrainz
import requests_mock
from re import compile
from test import _common


class ArgumentTest(_common.RequestsMockingTestCase):
    """Tests request methods to ensure they're enforcing general parameters
    (useragent, authentication)."""

    def setUp(self):
        super(ArgumentTest, self).setUp()
        musicbrainz.set_rate_limit(False)
        self.m.get(compile("ws/2/.*"), text="<response/>")

    def tearDown(self):
        musicbrainz.set_rate_limit(True)

    def test_no_client(self):
        musicbrainzngs.set_useragent("testapp", "0.1", "test@example.org")
        musicbrainz._mb_request(path="foo", client_required=False)
        self.assertFalse("testapp" in self.last_url)

    def test_client(self):
        musicbrainzngs.set_useragent("testapp", "0.1", "test@example.org")
        musicbrainz._mb_request(path="foo", client_required=True)
        self.assertTrue("testapp" in self.last_url)

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
        self.assertRaises(musicbrainzngs.UsageError, musicbrainz._mb_request,
                          path="foo")

    def test_auth_headers(self):
        musicbrainz._useragent = "test"
        musicbrainz.auth("user", "password")
        req = musicbrainz._mb_request(path="foo", auth_required=musicbrainz.AUTH_YES)
        assert(self.m.request_history[-1]._request.hooks['response'][0].__name__ == "handle_401")
        assert(self.m.request_history[-1]._request.hooks['response'][1].__name__ == "handle_redirect")

    def test_auth_headers_ifset(self):
        musicbrainz._useragent = "test"
        musicbrainz.auth("user", "password")
        req = musicbrainz._mb_request(path="foo", auth_required=musicbrainz.AUTH_IFSET)
        assert(self.m.request_history[-1]._request.hooks['response'][0].__name__ == "handle_401")
        assert(self.m.request_history[-1]._request.hooks['response'][1].__name__ == "handle_redirect")

    def test_auth_headers_ifset_no_user(self):
        musicbrainz._useragent = "test"
        musicbrainz.auth("", "")
        # if no user and password, auth is not set for AUTH_IFSET
        req = musicbrainz._mb_request(path="foo", auth_required=musicbrainz.AUTH_IFSET)
        assert not self.m.request_history[-1]._request.hooks['response']


class MethodTest(_common.RequestsMockingTestCase):
    """Tests the various _do_mb_* methods to ensure they're setting the
    using the correct HTTP method."""

    def setUp(self):
        super(MethodTest, self).setUp()
        musicbrainzngs.set_useragent("a", "1")
        musicbrainz.auth("user", "password")
        musicbrainz.set_rate_limit(False)
        self.m.register_uri(requests_mock.ANY, requests_mock.ANY,
                            text="<response/>")

    def tearDown(self):
        musicbrainz.set_rate_limit(False)

    def test_invalid_method(self):
        self.assertRaises(ValueError, musicbrainz._mb_request, path="foo",
                          method="HUG")

    def test_delete(self):
        musicbrainz._do_mb_delete("foo")
        self.assertEqual("DELETE", self.m.request_history.pop().method)

    def test_put(self):
        musicbrainz._do_mb_put("foo")
        self.assertEqual("PUT", self.m.request_history.pop().method)

    def test_post(self):
        musicbrainz._do_mb_post("foo", "body")
        self.assertEqual("POST", self.m.request_history.pop().method)

    def test_get(self):
        musicbrainz._do_mb_query("artist", 1234, [], [])
        self.assertEqual("GET", self.m.request_history.pop().method)


class HostnameTest(_common.RequestsMockingTestCase):
    """Test that the protocol, hostname, and port are set as expected"""

    def setUp(self):
        super(HostnameTest, self).setUp()
        musicbrainzngs.set_useragent("a", "1")
        musicbrainz.set_rate_limit(False)
        self.m.get(compile("ws/2/.*/.*"), text="<response/>")

    def tearDown(self):
        musicbrainz.set_rate_limit(True)
        musicbrainzngs.set_hostname("musicbrainz.org", use_https=True)

    def test_default_musicbrainz_https(self):
        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b")
        self.assertEqual("https://musicbrainz.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", self.last_url)

    def test_set_http(self):
        musicbrainzngs.set_hostname("beta.musicbrainz.org")

        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b")
        self.assertEqual("http://beta.musicbrainz.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", self.last_url)

    def test_set_https(self):
        musicbrainzngs.set_hostname("mbmirror.org", use_https=True)

        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b")
        self.assertEqual("https://mbmirror.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", self.last_url)

    def test_set_port(self):
        musicbrainzngs.set_hostname("localhost:8000", use_https=False)

        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b")
        self.assertEqual("http://localhost:8000/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", self.last_url)
