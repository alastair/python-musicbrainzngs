import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import musicbrainzngs
from musicbrainzngs import musicbrainz
from test import _common

class SubmitTest(unittest.TestCase):
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

