import musicbrainzngs
import requests_mock
from musicbrainzngs import musicbrainz
from test import _common


class SubmitTest(_common.RequestsMockingTestCase):
    def setUp(self):
        super(SubmitTest, self).setUp()
        self.m.register_uri(requests_mock.ANY, requests_mock.ANY, text="<response/>")
        musicbrainzngs.set_useragent("testapp", "0.1", "test@example.org")
        musicbrainz.auth("user", "password")
        musicbrainz.set_rate_limit(False)

    def tearDown(self):
        musicbrainz._useragent = ""
        musicbrainz._client = ""
        musicbrainz.user = ""
        musicbrainz.password = ""
        musicbrainz.set_rate_limit(True)

    def test_submit_tags(self):
        def make_xml(**kwargs):
            self.assertEqual({'artist_tags': {'mbid': ['one', 'two']}}, kwargs)
        oldmake_tag_request = musicbrainz.mbxml.make_tag_request
        musicbrainz.mbxml.make_tag_request = make_xml

        musicbrainz.submit_tags(artist_tags={"mbid": ["one", "two"]})
        musicbrainz.mbxml.make_tag_request = oldmake_tag_request

    def test_submit_single_tag(self):
        def make_xml(**kwargs):
            self.assertEqual({'artist_tags': {'mbid': ['single']}}, kwargs)
        oldmake_tag_request = musicbrainz.mbxml.make_tag_request
        musicbrainz.mbxml.make_tag_request = make_xml

        musicbrainz.submit_tags(artist_tags={"mbid": "single"})
        musicbrainz.mbxml.make_tag_request = oldmake_tag_request
