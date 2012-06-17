# Tests for parsing of release queries

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
        musicbrainzngs.set_useragent("test", "1")
        musicbrainzngs.set_rate_limit(False)

    def testGetRelease(self):
        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b")
        self.assertEqual("http://musicbrainz.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", _common.opener.get_url())

        # one include
        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", includes=["artists"])
        self.assertEqual("http://musicbrainz.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b?inc=artists", _common.opener.get_url())

        # more than one include
        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", includes=["artists", "recordings", "artist-credits"])
        expected = "http://musicbrainz.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b?inc=artists+recordings+artist-credits"
        self.assertEqual(expected, _common.opener.get_url())


class GetReleaseTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "release")

    def testArtistCredit(self):
        """
        If the artist credit is the same in the track and recording, make sure that
        the information is replicated in both objects, otherwise have distinct ones.
        """

        # If no artist-credit in the track, copy in the recording one
        fn = os.path.join(self.datadir, "833d4c3a-2635-4b7a-83c4-4e560588f23a-recordings+artist-credits.xml")
        res = mbxml.parse_message(open(fn))
        tracks = res["release"]["medium-list"][0]["track-list"]
        t1 = tracks[1]
        self.assertEqual(t1["artist-credit"], t1["recording"]["artist-credit"])
        self.assertEqual("JT Bruce", t1["artist-credit-phrase"])
        self.assertEqual(t1["recording"]["artist-credit-phrase"], t1["artist-credit-phrase"])

        # Recording AC is different to track AC
        fn = os.path.join(self.datadir, "fbe4490e-e366-4da2-a37a-82162d2f41a9-recordings+artist-credits.xml")
        res = mbxml.parse_message(open(fn))
        tracks = res["release"]["medium-list"][0]["track-list"]
        t1 = tracks[1]
        self.assertNotEqual(t1["artist-credit"], t1["recording"]["artist-credit"])
        self.assertEqual("H. Lichner", t1["artist-credit-phrase"])
        self.assertNotEqual(t1["recording"]["artist-credit-phrase"], t1["artist-credit-phrase"])

    def testTrackLength(self):
        """
        Test that if there is a track length, then `track_or_recording_length` has
        that, but if not then fill the value from the recording length
        """
        fn = os.path.join(self.datadir, "b66ebe6d-a577-4af8-9a2e-a029b2147716-recordings.xml")
        res = mbxml.parse_message(open(fn))
        tracks = res["release"]["medium-list"][0]["track-list"]

        # No track length and recording length
        t1 = tracks[0]
        self.assertTrue("length" not in t1)
        self.assertEqual("180000", t1["recording"]["length"])
        self.assertEqual("180000", t1["track_or_recording_length"])

        # Track length and recording length same
        t2 = tracks[1]
        self.assertEqual("279000", t2["length"])
        self.assertEqual("279000", t2["recording"]["length"])
        self.assertEqual("279000", t2["track_or_recording_length"])

        # Track length and recording length different
        t3 = tracks[2]
        self.assertEqual("60000", t3["length"])
        self.assertEqual("80000", t3["recording"]["length"])
        self.assertEqual("60000", t3["track_or_recording_length"])

        # No track lengths
        t4 = tracks[3]
        self.assertTrue("length" not in t4["recording"])
        self.assertTrue("length" not in t4)
        self.assertTrue("track_or_recording_length" not in t4)

    def testTrackTitle(self):
        pass

    def testTrackNumber(self):
        """
        Test that track number (number or text) and track position (always an increasing number)
        are both read properly
        """
        fn = os.path.join(self.datadir, "212895ca-ee36-439a-a824-d2620cd10461-recordings.xml")
        res = mbxml.parse_message(open(fn))
        tracks = res["release"]["medium-list"][0]["track-list"]
        # This release doesn't number intro tracks as numbered tracks,
        # so position and number get 'out of sync'
        self.assertEqual(['1', '2', '3'], [t["position"] for t in tracks[:3]])
        self.assertEqual(['', '1', '2'], [t["number"] for t in tracks[:3]])

        fn = os.path.join(self.datadir, "a81f3c15-2f36-47c7-9b0f-f684a8b0530f-recordings.xml")
        res = mbxml.parse_message(open(fn))
        tracks = res["release"]["medium-list"][0]["track-list"]
        self.assertEqual(['1', '2'], [t["position"] for t in tracks])
        self.assertEqual(['A', 'B'], [t["number"] for t in tracks])

