import unittest
import musicbrainzngs
from musicbrainzngs import musicbrainz
import requests_mock
from musicbrainzngs import mbxml
from re import compile
from test import _common


class ArgumentTest(_common.RequestsMockingTestCase):
    """Tests request methods to ensure they're enforcing general parameters
    (useragent, authentication)."""

    def setUp(self):
        super(ArgumentTest, self).setUp()
        self.m.get(compile("ws/2/.*"), text="<response/>")

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
        musicbrainz.user = ""
        self.assertRaises(musicbrainzngs.UsageError, musicbrainz._mb_request,
                          path="foo", auth_required=musicbrainz.AUTH_YES)

    def test_missing_useragent(self):
        musicbrainz._useragent = ""
        self.assertRaises(musicbrainzngs.UsageError, musicbrainz._mb_request,
                          path="foo")


class MethodTest(_common.RequestsMockingTestCase):
    """Tests the various _do_mb_* methods to ensure they're setting the
    using the correct HTTP method."""

    def setUp(self):
        super(MethodTest, self).setUp()
        musicbrainz.auth("user", "password")
        self.m.register_uri(requests_mock.ANY, requests_mock.ANY,
                            text="<response/>")

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
