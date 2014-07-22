import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import musicbrainzngs
from musicbrainzngs import compat
from test import _common

class CollectionTest(unittest.TestCase):
    """ Test that requesting collections works properly """

    def setUp(self):
        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)

    def test_auth_required(self):
        """ Check the auth_required method in isolation """
        ar = musicbrainzngs.musicbrainz._is_auth_required("collection", "", [])
        self.assertEquals(True, ar)

        ar = musicbrainzngs.musicbrainz._is_auth_required("collection", "foo/releases", [])
        self.assertEquals(False, ar)

    def test_my_collections(self):
        """ If you ask for your collections, you need to have
        authenticated first."""

        old_mb_request = musicbrainzngs.musicbrainz._mb_request

        params = {}
        def local_mb_request(path, method='GET', auth_required=False,
                client_required=False, args=None, data=None, body=None):
            params["auth_required"] = auth_required

        musicbrainzngs.musicbrainz._mb_request = local_mb_request
        musicbrainzngs.get_collections()
        self.assertEqual(True, params["auth_required"])

        musicbrainzngs.musicbrainz._mb_request = old_mb_request

    def test_other_collection(self):
        """ If you ask for someone else's collection, you don't
        need to be authenticated."""

        old_mb_request = musicbrainzngs.musicbrainz._mb_request

        params = {}
        def local_mb_request(path, method='GET', auth_required=False,
                client_required=False, args=None, data=None, body=None):
            params["auth_required"] = auth_required

        musicbrainzngs.musicbrainz._mb_request = local_mb_request
        musicbrainzngs.get_releases_in_collection("17905fdb-102d-40f0-91d3-eabcabc64fd3")
        self.assertEqual(False, params["auth_required"])

        musicbrainzngs.musicbrainz._mb_request = old_mb_request

    def test_no_collection(self):
        """ If a collection doesn't exist, you get a 404 """

        exc = compat.HTTPError("", 404, "", "", _common.StringIO.StringIO(""))
        self.opener = _common.FakeOpener(exception=musicbrainzngs.ResponseError(cause=exc))
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        try:
            res = musicbrainzngs.get_releases_in_collection("17905fdb-102d-40f0-91d3-eabcabc64f44")
            self.assertTrue(False, "Expected an exception")
        except musicbrainzngs.ResponseError as e:
            self.assertEqual(e.cause.code, 404)

    def test_private_collection(self):
        """ If you ask for a collection that is private, you should
        get a 401"""

        exc = compat.HTTPError("", 401, "", "", _common.StringIO.StringIO(""))
        self.opener = _common.FakeOpener(exception=musicbrainzngs.AuthenticationError(cause=exc))
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        try:
            res = musicbrainzngs.get_releases_in_collection("17905fdb-102d-40f0-91d3-eabcabc64fd3")
            self.assertTrue(False, "Expected an exception")
        except musicbrainzngs.AuthenticationError as e:
            self.assertEqual(e.cause.code, 401)
