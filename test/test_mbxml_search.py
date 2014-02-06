import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import musicbrainzngs
from musicbrainzngs import mbxml
from test import _common


class UrlTest(unittest.TestCase):
    """ Test that the correct URL is generated when a search query is made """

    def setUp(self):
        self.opener = _common.FakeOpener("<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener

        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)

    def testSearchArtist(self):
        musicbrainzngs.search_artists("Dynamo Go")
        self.assertEqual("http://musicbrainz.org/ws/2/artist/?query=Dynamo+Go", self.opener.get_url())

    def testSearchWork(self):
        musicbrainzngs.search_works("Fountain City")
        self.assertEqual("http://musicbrainz.org/ws/2/work/?query=Fountain+City", self.opener.get_url())

    def testSearchLabel(self):
        musicbrainzngs.search_labels("Waysafe")
        self.assertEqual("http://musicbrainz.org/ws/2/label/?query=Waysafe", self.opener.get_url())

    def testSearchRelease(self):
        musicbrainzngs.search_releases("Affordable Pop Music")
        self.assertEqual("http://musicbrainz.org/ws/2/release/?query=Affordable+Pop+Music", self.opener.get_url())

    def testSearchReleaseGroup(self):
        musicbrainzngs.search_release_groups("Affordable Pop Music")
        self.assertEqual("http://musicbrainz.org/ws/2/release-group/?query=Affordable+Pop+Music", self.opener.get_url())

    def testSearchRecording(self):
        musicbrainzngs.search_recordings("Thief of Hearts")
        self.assertEqual("http://musicbrainz.org/ws/2/recording/?query=Thief+of+Hearts", self.opener.get_url())

class SearchArtistTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(os.path.dirname(__file__), "data", "search-artist.xml")
        res = mbxml.parse_message(open(fn))
        self.assertEqual(25, len(res["artist-list"]))
        self.assertEqual(349, res["artist-count"])
        one = res["artist-list"][0]
        self.assertEqual(9, len(one.keys()))
        # Score is a key that is only in search results -
        # so check for it here
        self.assertEqual("100", one["ext:score"])

class SearchReleaseTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(os.path.dirname(__file__), "data", "search-release.xml")
        res = mbxml.parse_message(open(fn))
        self.assertEqual(25, len(res["release-list"]))
        self.assertEqual(16739, res["release-count"])
        one = res["release-list"][0]
        self.assertEqual("100", one["ext:score"])

class SearchReleaseGroupTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(os.path.dirname(__file__), "data", "search-release-group.xml")
        res = mbxml.parse_message(open(fn))
        self.assertEqual(25, len(res["release-group-list"]))
        self.assertEqual(14641, res["release-group-count"])
        one = res["release-group-list"][0]
        self.assertEqual("100", one["ext:score"])

class SearchWorkTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(os.path.dirname(__file__), "data", "search-work.xml")
        res = mbxml.parse_message(open(fn))
        self.assertEqual(25, len(res["work-list"]))
        self.assertEqual(174, res["work-count"])
        one = res["work-list"][0]
        self.assertEqual("100", one["ext:score"])

class SearchLabelTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(os.path.dirname(__file__), "data", "search-label.xml")
        res = mbxml.parse_message(open(fn))
        self.assertEqual(1, len(res["label-list"]))
        self.assertEqual(1, res["label-count"])
        one = res["label-list"][0]
        self.assertEqual("100", one["ext:score"])

class SearchRecordingTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(os.path.dirname(__file__), "data", "search-recording.xml")
        res = mbxml.parse_message(open(fn))
        self.assertEqual(25, len(res["recording-list"]))
        self.assertEqual(1258, res["recording-count"])
        one = res["recording-list"][0]
        self.assertEqual("100", one["ext:score"])
