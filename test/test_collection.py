import unittest
import musicbrainzngs
from musicbrainzngs import compat
from test import _common
import requests_mock
from re import compile


class CollectionTest(unittest.TestCase):
    """ Test that requesting collections works properly """

    def setUp(self):
        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)

    def tearDown(self):
        musicbrainzngs.set_rate_limit(True)

    def test_auth_required(self):
        """ Check the auth_required method in isolation """
        ar = musicbrainzngs.musicbrainz._get_auth_type("collection", "", [])
        self.assertEqual(musicbrainzngs.musicbrainz.AUTH_YES, ar)

        ar = musicbrainzngs.musicbrainz._get_auth_type("collection",
                                                       "foo/releases", [])
        self.assertEqual(musicbrainzngs.musicbrainz.AUTH_IFSET, ar)

        ar = musicbrainzngs.musicbrainz._get_auth_type("artist", "5b11f4ce-a62d-471e-81fc-a69a8278c7da", [])
        self.assertEqual(musicbrainzngs.musicbrainz.AUTH_NO, ar)

        ar = musicbrainzngs.musicbrainz._get_auth_type("artist", "5b11f4ce-a62d-471e-81fc-a69a8278c7da", ["user-tags"])
        self.assertEqual(musicbrainzngs.musicbrainz.AUTH_YES, ar)

        ar = musicbrainzngs.musicbrainz._get_auth_type("artist", "5b11f4ce-a62d-471e-81fc-a69a8278c7da", ["aliases", "user-genres", "artist-rels"])
        self.assertEqual(musicbrainzngs.musicbrainz.AUTH_YES, ar)

    def test_my_collections(self):
        """ If you ask for your collections, you need to have
        authenticated first."""

        old_mb_request = musicbrainzngs.musicbrainz._mb_request

        params = {}
        def local_mb_request(path, method='GET',
                auth_required=musicbrainzngs.musicbrainz.AUTH_NO,
                client_required=False, args=None, data=None, body=None):
            params["auth_required"] = auth_required

        musicbrainzngs.musicbrainz._mb_request = local_mb_request
        musicbrainzngs.get_collections()
        self.assertEqual(musicbrainzngs.musicbrainz.AUTH_YES,
                         params["auth_required"])

        musicbrainzngs.musicbrainz._mb_request = old_mb_request

    def test_other_collection(self):
        """ If you ask for someone else's collection, you don't
        need to be authenticated."""

        old_mb_request = musicbrainzngs.musicbrainz._mb_request

        params = {}
        def local_mb_request(path, method='GET',
                auth_required=musicbrainzngs.musicbrainz.AUTH_NO,
                client_required=False, args=None, data=None, body=None):
            params["auth_required"] = auth_required

        musicbrainzngs.musicbrainz._mb_request = local_mb_request
        musicbrainzngs.get_releases_in_collection(
                "17905fdb-102d-40f0-91d3-eabcabc64fd3")
        # If _get_auth_type() returns AUTH_IFSET, then _mb_request()
        # should send the user credentials if they are set by auth()
        # i.e., We use whether auth() has been executed to determine if
        # the requested collection belongs to the user or not.
        self.assertEqual(musicbrainzngs.musicbrainz.AUTH_IFSET,
                         params["auth_required"])

        musicbrainzngs.musicbrainz._mb_request = old_mb_request

    @requests_mock.Mocker()
    def test_no_collection(self, m):
        """ If a collection doesn't exist, you get a 404 """
        m.get(compile("ws/2/collection/17905fdb-102d-40f0-91d3-eabcabc64f44"),
              status_code=404)

        try:
            res = musicbrainzngs.get_releases_in_collection("17905fdb-102d-40f0-91d3-eabcabc64f44")
            self.assertTrue(False, "Expected an exception")
        except musicbrainzngs.ResponseError as e:
            self.assertEqual(e.cause.response.status_code, 404)

    @requests_mock.Mocker()
    def test_private_collection(self, m):
        """ If you ask for a collection that is private, you should
        get a 401"""
        m.get(compile("ws/2/collection/17905fdb-102d-40f0-91d3-eabcabc64fd3"),
              status_code=401)

        try:
            res = musicbrainzngs.get_releases_in_collection("17905fdb-102d-40f0-91d3-eabcabc64fd3")
            self.assertTrue(False, "Expected an exception")
        except musicbrainzngs.AuthenticationError as e:
            self.assertEqual(e.cause.response.status_code, 401)
