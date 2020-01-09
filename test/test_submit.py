import unittest
import musicbrainzngs
from musicbrainzngs import musicbrainz
from test import _common


class SubmitTest(unittest.TestCase):

    def setUp(self):
        self.orig_opener = musicbrainzngs.compat.build_opener
        musicbrainz.set_useragent("test_client", "1.0")
        musicbrainz.auth("user", "password")
        musicbrainz.set_rate_limit(False)

    def tearDown(self):
        musicbrainzngs.compat.build_opener = self.orig_opener
        musicbrainz._useragent = ""
        musicbrainz._client = ""
        musicbrainz.user = ""
        musicbrainz.password = ""
        musicbrainz.set_rate_limit(True)

    def test_submit_tags(self):
        self.opener = _common.FakeOpener("<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        def make_xml(**kwargs):
            self.assertEqual({'artist_tags': {'mbid': ['one', 'two']}}, kwargs)
        oldmake_tag_request = musicbrainz.mbxml.make_tag_request
        musicbrainz.mbxml.make_tag_request = make_xml

        musicbrainz.submit_tags(artist_tags={"mbid": ["one", "two"]})
        musicbrainz.mbxml.make_tag_request = oldmake_tag_request

    def test_submit_single_tag(self):
        self.opener = _common.FakeOpener("<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        def make_xml(**kwargs):
            self.assertEqual({'artist_tags': {'mbid': ['single']}}, kwargs)
        oldmake_tag_request = musicbrainz.mbxml.make_tag_request
        musicbrainz.mbxml.make_tag_request = make_xml

        musicbrainz.submit_tags(artist_tags={"mbid": "single"})
        musicbrainz.mbxml.make_tag_request = oldmake_tag_request

