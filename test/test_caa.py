import unittest

from musicbrainzngs import caa
from musicbrainzngs import compat
from musicbrainzngs.musicbrainz import _version
import musicbrainzngs
from test import _common


class CaaTest(unittest.TestCase):

    def test_get_list(self):
        # check the url and response for a listing
        resp = b'{"images":[]}'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.get_image_list("8ec178f4-a8e8-4f22-bcba-1964466ef214")
        self.assertEqual("https://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214", self.opener.myurl)
        self.assertEqual(1, len(res))
        self.assertTrue("images" in res)

    def test_get_release_group_list(self):
        # check the url and response for a listing
        resp = b'{"images":[], "release": "foo"}'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.get_release_group_image_list("8ec178f4-a8e8-4f22-bcba-1964466ef214")
        self.assertEqual("https://coverartarchive.org/release-group/8ec178f4-a8e8-4f22-bcba-1964466ef214", self.opener.myurl)
        self.assertEqual(2, len(res))
        self.assertTrue("images" in res)
        self.assertEqual("foo", res["release"])

    def test_list_none(self):
        """ When CAA gives a 404 error, pass it through."""

        exc = compat.HTTPError("", 404, "", "", _common.StringIO.StringIO(""))
        self.opener = _common.FakeOpener(exception=musicbrainzngs.ResponseError(cause=exc))
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        try:
            res = caa.get_image_list("8ec178f4-a8e8-4f22-bcba-19644XXXXXX")
            self.assertTrue(False, "Expected an exception")
        except musicbrainzngs.ResponseError as e:
            self.assertEqual(e.cause.code, 404)

    def test_list_baduuid(self):
        exc = compat.HTTPError("", 400, "", "", _common.StringIO.StringIO(""))
        self.opener = _common.FakeOpener(exception=musicbrainzngs.ResponseError(cause=exc))
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        try:
            res = caa.get_image_list("8ec178f4-a8e8-4f22-bcba-19644XXXXXX")
            self.assertTrue(False, "Expected an exception")
        except musicbrainzngs.ResponseError as e:
            self.assertEqual(e.cause.code, 400)

    def test_set_useragent(self):
        """ When a useragent is set it is sent with the request """
        musicbrainzngs.set_useragent("caa-test", "0.1")

        resp = b'{"images":[]}'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.get_image_list("8ec178f4-a8e8-4f22-bcba-1964466ef214")

        headers = dict(self.opener.headers)
        self.assertTrue("User-agent" in headers)
        self.assertEqual("caa-test/0.1 python-musicbrainzngs/%s" % _version, headers["User-agent"])

    def test_coverid(self):
        resp = b'some_image'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.get_image("8ec178f4-a8e8-4f22-bcba-1964466ef214", "1234")

        self.assertEqual("https://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/1234", self.opener.myurl)
        self.assertEqual(resp, res)

    def test_get_size(self):
        resp = b'some_image'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.get_image("8ec178f4-a8e8-4f22-bcba-1964466ef214", "1234", 250)

        self.assertEqual("https://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/1234-250", self.opener.myurl)
        self.assertEqual(resp, res)

    def test_front(self):
        resp = b'front_image'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.get_image_front("8ec178f4-a8e8-4f22-bcba-1964466ef214")

        self.assertEqual("https://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/front", self.opener.myurl)
        self.assertEqual(resp, res)

    def test_release_group_front(self):
        resp = b'front_image'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.get_release_group_image_front("8ec178f4-a8e8-4f22-bcba-1964466ef214")

        self.assertEqual("https://coverartarchive.org/release-group/8ec178f4-a8e8-4f22-bcba-1964466ef214/front", self.opener.myurl)
        self.assertEqual(resp, res)

    def test_back(self):
        resp = b'back_image'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.get_image_back("8ec178f4-a8e8-4f22-bcba-1964466ef214")

        self.assertEqual("https://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/back", self.opener.myurl)
        self.assertEqual(resp, res)

