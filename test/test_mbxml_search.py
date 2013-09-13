import musicbrainzngs
import unittest
import os
from musicbrainzngs import mbxml
from test import _common
from re import compile


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class UrlTest(_common.RequestsMockingTestCase):
    """ Test that the correct URL is generated when a search query is made """

    def setUp(self):
        super(UrlTest, self).setUp()

        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)

        self.m.get(compile("ws/2/.*/.*"), text="<response/>")

    def testSearchArtist(self):
        musicbrainzngs.search_artists("Dynamo Go")
        self.assertEqual("https://musicbrainz.org/ws/2/artist/?query=Dynamo+Go",
                         self.last_url)

    def testSearchEvent(self):
        musicbrainzngs.search_events("woodstock")
        self.assertEqual("https://musicbrainz.org/ws/2/event/?query=woodstock",
                         self.last_url)

    def testSearchLabel(self):
        musicbrainzngs.search_labels("Waysafe")
        self.assertEqual("https://musicbrainz.org/ws/2/label/?query=Waysafe",
                         self.last_url)

    def testSearchPlace(self):
        musicbrainzngs.search_places("Fillmore")
        self.assertEqual("https://musicbrainz.org/ws/2/place/?query=Fillmore",
                         self.last_url)

    def testSearchRelease(self):
        musicbrainzngs.search_releases("Affordable Pop Music")
        self.assertEqual("https://musicbrainz.org/ws/2/release/?query=Affordable+Pop+Music",
                         self.last_url)

    def testSearchReleaseGroup(self):
        musicbrainzngs.search_release_groups("Affordable Pop Music")
        self.assertEqual("https://musicbrainz.org/ws/2/release-group/?query=Affordable+Pop+Music",
                         self.last_url)

    def testSearchRecording(self):
        musicbrainzngs.search_recordings("Thief of Hearts")
        self.assertEqual("https://musicbrainz.org/ws/2/recording/?query=Thief+of+Hearts",
                         self.last_url)

    def testSearchWork(self):
        musicbrainzngs.search_works("Fountain City")
        self.assertEqual("https://musicbrainz.org/ws/2/work/?query=Fountain+City",
                         self.last_url)


class SearchArtistTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-artist.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg)
        self.assertEqual(25, len(res["artist-list"]))
        self.assertEqual(349, res["artist-count"])
        one = res["artist-list"][0]
        self.assertEqual(9, len(one.keys()))
        # Score is a key that is only in search results -
        # so check for it here
        self.assertEqual("100", one["ext:score"])


class SearchReleaseTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-release.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg)
        self.assertEqual(25, len(res["release-list"]))
        self.assertEqual(16739, res["release-count"])
        one = res["release-list"][0]
        self.assertEqual("100", one["ext:score"])

        # search results have a medium-list/track-count element
        self.assertEqual(4, one["medium-track-count"])
        self.assertEqual(1, one["medium-count"])
        self.assertEqual("CD", one["medium-list"][0]["format"])


class SearchReleaseGroupTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-release-group.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg)
        self.assertEqual(25, len(res["release-group-list"]))
        self.assertEqual(14641, res["release-group-count"])
        one = res["release-group-list"][0]
        self.assertEqual("100", one["ext:score"])


class SearchWorkTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-work.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg)
        self.assertEqual(25, len(res["work-list"]))
        self.assertEqual(174, res["work-count"])
        one = res["work-list"][0]
        self.assertEqual("100", one["ext:score"])


class SearchLabelTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-label.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg)
        self.assertEqual(1, len(res["label-list"]))
        self.assertEqual(1, res["label-count"])
        one = res["label-list"][0]
        self.assertEqual("100", one["ext:score"])


class SearchRecordingTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-recording.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg)
        self.assertEqual(25, len(res["recording-list"]))
        self.assertEqual(1258, res["recording-count"])
        one = res["recording-list"][0]
        self.assertEqual("100", one["ext:score"])


class SearchInstrumentTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-instrument.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg)
        self.assertEqual(23, len(res["instrument-list"]))
        self.assertEqual(23, res["instrument-count"])
        one = res["instrument-list"][0]
        self.assertEqual("100", one["ext:score"])
        end = res["instrument-list"][-1]
        self.assertEqual("29", end["ext:score"])


class SearchPlaceTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-place.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg)
        self.assertEqual(14, res["place-count"])
        self.assertEqual(14, len(res["place-list"]))
        one = res["place-list"][0]
        self.assertEqual("100", one["ext:score"])
        two = res["place-list"][1]
        self.assertEqual("63", two["ext:score"])
        self.assertEqual("Southampton", two["disambiguation"])


class SearchEventTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-event.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg)
        self.assertEqual(3, res["event-count"])
        self.assertEqual(3, len(res["event-list"]))
        one = res["event-list"][0]
        self.assertEqual("100", one["ext:score"])
        two = res["event-list"][1]
        self.assertEqual(1, len(two["place-relation-list"]))
