# Tests for parsing of release queries

import unittest
import os
import musicbrainzngs
from test import _common
import requests_mock
from re import compile


class UrlTest(_common.RequestsMockingTestCase):
    """ Test that the correct URL is generated when a search query is made """

    def setUp(self):
        super(UrlTest, self).setUp()

        musicbrainzngs.set_useragent("test", "1")
        musicbrainzngs.set_rate_limit(False)
        self.m.get(compile("ws/2/.*/.*"), text="<response/>")

    def tearDown(self):
        musicbrainzngs.set_rate_limit(True)

    def testGetRelease(self):
        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b")
        self.assertEqual("https://musicbrainz.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", self.last_url)

        # one include
        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", includes=["artists"])
        self.assertEqual("https://musicbrainz.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b?inc=artists", self.last_url)

        # more than one include
        musicbrainzngs.get_release_by_id("5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b", includes=["artists", "recordings", "artist-credits"])
        expected = "https://musicbrainz.org/ws/2/release/5e3524ca-b4a1-4e51-9ba5-63ea2de8f49b?inc=artists+recordings+artist-credits"
        self.assertEqual(expected, self.last_url)


class GetReleaseTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "release")

    def testArtistCredit(self):
        """
        If the artist credit is the same in the track and recording, make sure that
        the information is replicated in both objects, otherwise have distinct ones.
        """

        # If no artist-credit in the track, copy in the recording one
        res = _common.open_and_parse_test_data(self.datadir, "833d4c3a-2635-4b7a-83c4-4e560588f23a-recordings+artist-credits.xml")
        tracks = res["release"]["medium-list"][0]["track-list"]
        t1 = tracks[1]
        self.assertEqual(t1["artist-credit"], t1["recording"]["artist-credit"])
        self.assertEqual("JT Bruce", t1["artist-credit-phrase"])
        self.assertEqual(t1["recording"]["artist-credit-phrase"], t1["artist-credit-phrase"])

        # Recording AC is different to track AC
        res = _common.open_and_parse_test_data(self.datadir, "fbe4490e-e366-4da2-a37a-82162d2f41a9-recordings+artist-credits.xml")
        tracks = res["release"]["medium-list"][0]["track-list"]
        t1 = tracks[1]
        self.assertNotEqual(t1["artist-credit"], t1["recording"]["artist-credit"])
        self.assertEqual("H. Lichner", t1["artist-credit-phrase"])
        self.assertNotEqual(t1["recording"]["artist-credit-phrase"], t1["artist-credit-phrase"])

    def testTrackId(self):
        """
        Test that the id attribute of tracks is read.
        """
        res = _common.open_and_parse_test_data(self.datadir, "212895ca-ee36-439a-a824-d2620cd10461-recordings.xml")
        tracks = res["release"]["medium-list"][0]["track-list"]
        map(lambda t: self.assertTrue("id" in t), tracks)

    def testTrackLength(self):
        """
        Test that if there is a track length, then `track_or_recording_length` has
        that, but if not then fill the value from the recording length
        """
        res = _common.open_and_parse_test_data(self.datadir, "b66ebe6d-a577-4af8-9a2e-a029b2147716-recordings.xml")
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
        res = _common.open_and_parse_test_data(self.datadir, "212895ca-ee36-439a-a824-d2620cd10461-recordings.xml")
        tracks = res["release"]["medium-list"][0]["track-list"]
        # This release doesn't number intro tracks as numbered tracks,
        # so position and number get 'out of sync'
        self.assertEqual(['1', '2', '3'], [t["position"] for t in tracks[:3]])
        self.assertEqual(['', '1', '2'], [t["number"] for t in tracks[:3]])

        res = _common.open_and_parse_test_data(self.datadir, "a81f3c15-2f36-47c7-9b0f-f684a8b0530f-recordings.xml")
        tracks = res["release"]["medium-list"][0]["track-list"]
        self.assertEqual(['1', '2'], [t["position"] for t in tracks])
        self.assertEqual(['A', 'B'], [t["number"] for t in tracks])

        res = _common.open_and_parse_test_data(self.datadir, "9ce41d09-40e4-4d33-af0c-7fed1e558dba-recordings.xml")
        tracks = res["release"]["medium-list"][0]["data-track-list"]
        self.assertEqual(list(map(str, range(1, 199))), [t["position"] for t in tracks])
        self.assertEqual(list(map(str, range(1, 199))), [t["number"] for t in tracks])

    def testVideo(self):
        """
        Test that the video attribute is parsed.
        """
        res = _common.open_and_parse_test_data(self.datadir, "fe29e7f0-eb46-44ba-9348-694166f47885-recordings.xml")
        trackswithoutvideo = res["release"]["medium-list"][0]["track-list"]
        trackswithvideo = res["release"]["medium-list"][2]["track-list"]
        map(lambda t: self.assertTrue("video" not in ["recording"]), trackswithoutvideo)
        map(lambda t: self.assertEqual("true", t["recording"]["video"]), trackswithvideo)

    def testPregapTrack(self):
        """
        Test that the pregap track is parsed if it exists.
        """
        res = _common.open_and_parse_test_data(self.datadir, "8eb2b179-643d-3507-b64c-29fcc6745156-recordings.xml")
        medium = res["release"]["medium-list"][0]
        self.assertTrue("pregap" in medium)
        self.assertEqual("0", medium["pregap"]["position"])
        self.assertEqual("0", medium["pregap"]["number"])
        self.assertEqual("35000", medium["pregap"]["length"])
        self.assertEqual("[untitled]", medium["pregap"]["recording"]["title"])

    def testDataTracklist(self):
        """
        Test that data tracklist are parsed.
        """
        res = _common.open_and_parse_test_data(self.datadir, "9ce41d09-40e4-4d33-af0c-7fed1e558dba-recordings.xml")
        medium = res["release"]["medium-list"][0]
        self.assertTrue("data-track-list" in medium)
        self.assertEqual(198, len(medium["data-track-list"]))
