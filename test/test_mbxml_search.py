import unittest
import os
from musicbrainzngs import mbxml


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


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
