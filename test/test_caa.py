import unittest

from musicbrainzngs import caa
from musicbrainzngs import compat
from musicbrainzngs.musicbrainz import _version
import musicbrainzngs
from test import _common
import requests_mock
from re import compile

@requests_mock.Mocker()
class CaaTest(unittest.TestCase):
    def setUp(self):
        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)

    def test_get_list(self, m):
        # check the url and response for a listing
        resp = '{"images":[]}'
        m.get(compile("coverartarchive.org/"), text=resp)
        res = caa.get_image_list("8ec178f4-a8e8-4f22-bcba-1964466ef214")
        self.assertEqual("https://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214", m.request_history.pop().url)
        self.assertEqual(1, len(res))
        self.assertTrue("images" in res)

    def test_get_release_group_list(self, m):
        # check the url and response for a listing
        resp = '{"images":[], "release": "foo"}'
        m.get(compile("coverartarchive.org/"), text=resp)
        res = caa.get_release_group_image_list("8ec178f4-a8e8-4f22-bcba-1964466ef214")
        self.assertEqual("https://coverartarchive.org/release-group/8ec178f4-a8e8-4f22-bcba-1964466ef214", m.request_history.pop().url)
        self.assertEqual(2, len(res))
        self.assertTrue("images" in res)
        self.assertEqual("foo", res["release"])

    def test_list_none(self, m):
        """ When CAA gives a 404 error, pass it through."""
        m.get(compile("coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-19644XXXXXX"),
              status_code=404)

        try:
            res = caa.get_image_list("8ec178f4-a8e8-4f22-bcba-19644XXXXXX")
            self.assertTrue(False, "Expected an exception")
        except musicbrainzngs.ResponseError as e:
            self.assertEqual(e.cause.response.status_code, 404)

    def test_list_baduuid(self, m):
        m.get(compile("coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-19644XXXXXX"),
              status_code=400)
        try:
            res = caa.get_image_list("8ec178f4-a8e8-4f22-bcba-19644XXXXXX")
            self.assertTrue(False, "Expected an exception")
        except musicbrainzngs.ResponseError as e:
            self.assertEqual(e.cause.response.status_code, 400)

    def test_set_useragent(self, m):
        """ When a useragent is set it is sent with the request """
        musicbrainzngs.set_useragent("caa-test", "0.1")

        resp = '{"images":[]}'
        m.get(compile("coverartarchive.org/"), text=resp)
        res = caa.get_image_list("8ec178f4-a8e8-4f22-bcba-1964466ef214")

        headers = dict(m.request_history.pop().headers)
        self.assertTrue("User-Agent" in headers)
        self.assertEqual("caa-test/0.1 python-musicbrainzngs/%s" % _version,
                         headers["User-Agent"])

    def test_coverid(self, m):
        resp = b'some_image'
        m.get(compile("coverartarchive.org/"), content=resp)
        res = caa.get_image("8ec178f4-a8e8-4f22-bcba-1964466ef214", "1234")

        self.assertEqual("https://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/1234", m.request_history.pop().url)
        self.assertEqual(resp, res)

    def test_get_size(self, m):
        resp = b'some_image'
        m.get(compile("coverartarchive.org/"), content=resp)
        res = caa.get_image("8ec178f4-a8e8-4f22-bcba-1964466ef214", "1234", 250)

        self.assertEqual("https://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/1234-250", m.request_history.pop().url)
        self.assertEqual(resp, res)

    def test_front(self, m):
        resp = b'front_image'
        m.get(compile("coverartarchive.org/"), content=resp)
        res = caa.get_image_front("8ec178f4-a8e8-4f22-bcba-1964466ef214")

        self.assertEqual("https://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/front", m.request_history.pop().url)
        self.assertEqual(resp, res)

    def test_release_group_front(self, m):
        resp = b'front_image'
        m.get(compile("coverartarchive.org/"), content=resp)
        res = caa.get_release_group_image_front("8ec178f4-a8e8-4f22-bcba-1964466ef214")

        self.assertEqual("https://coverartarchive.org/release-group/8ec178f4-a8e8-4f22-bcba-1964466ef214/front", m.request_history.pop().url)
        self.assertEqual(resp, res)

    def test_back(self, m):
        resp = b'back_image'
        m.get(compile("coverartarchive.org/"), content=resp)
        res = caa.get_image_back("8ec178f4-a8e8-4f22-bcba-1964466ef214")

        self.assertEqual("https://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/back", m.request_history.pop().url)
        self.assertEqual(resp, res)
