import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import musicbrainzngs
from musicbrainzngs import musicbrainz
from test import _common


class ArgumentTest(unittest.TestCase):
    """Tests request methods to ensure they're enforcing general parameters
    (useragent, authentication)."""

    def setUp(self):
        self.opener = _common.FakeOpener("<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener

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
        self.assertRaises(musicbrainzngs.UsageError,
                musicbrainz._mb_request, path="foo",
                auth_required=musicbrainz.AUTH_YES)

    def test_missing_useragent(self):
        musicbrainz._useragent = ""
        self.assertRaises(musicbrainzngs.UsageError,
                musicbrainz._mb_request, path="foo")


class MethodTest(unittest.TestCase):
    """Tests the various _do_mb_* methods to ensure they're setting the
    using the correct HTTP method."""

    def setUp(self):
        self.opener = _common.FakeOpener("<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener

        musicbrainz.auth("user", "password")

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
