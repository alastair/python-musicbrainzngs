# Tests for parsing of discid queries

import unittest
import os
import musicbrainzngs
import requests_mock
from re import compile
from test import _common


class UrlTest(unittest.TestCase):
    """ Test that the correct URL is generated when a search query is made """

    def setUp(self):
        musicbrainzngs.set_useragent("test", "1")
        musicbrainzngs.set_rate_limit(False)

    def tearDown(self):
        musicbrainzngs.set_rate_limit(True)

    @requests_mock.Mocker()
    def testGetDiscId(self, m):
        m.get(compile("musicbrainz.org/ws/2/discid"), text="<response/>")

        musicbrainzngs.get_releases_by_discid("xp5tz6rE4OHrBafj0bLfDRMGK48-")
        self.assertEqual("https://musicbrainz.org/ws/2/discid/xp5tz6rE4OHrBafj0bLfDRMGK48-",
                         m.request_history.pop().url)

        # one include
        musicbrainzngs.get_releases_by_discid("xp5tz6rE4OHrBafj0bLfDRMGK48-",
                includes=["recordings"])
        self.assertEqual("https://musicbrainz.org/ws/2/discid/xp5tz6rE4OHrBafj0bLfDRMGK48-?inc=recordings", m.request_history.pop().url)

        # more than one include
        musicbrainzngs.get_releases_by_discid("xp5tz6rE4OHrBafj0bLfDRMGK48-", includes=["artists", "recordings", "artist-credits"])
        expected = "https://musicbrainz.org/ws/2/discid/xp5tz6rE4OHrBafj0bLfDRMGK48-?inc=artists+recordings+artist-credits"
        self.assertEqual(expected, m.request_history.pop().url)


class GetDiscIdTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "discid")

    def testDiscId(self):
        """
        Test that the id attribute of the disc is read.
        """
        res = _common.open_and_parse_test_data(self.datadir, "xp5tz6rE4OHrBafj0bLfDRMGK48-.xml")
        self.assertEqual(res["disc"]["id"], "xp5tz6rE4OHrBafj0bLfDRMGK48-")

    def testTrackCount(self):
        """
        Test that the number of tracks (offset-count) is returned.
        """

        # discid without pregap track
        res = _common.open_and_parse_test_data(self.datadir, "xp5tz6rE4OHrBafj0bLfDRMGK48-.xml")
        self.assertEqual(res["disc"]["offset-count"], 8)

        # discid with pregap track
        # (the number of tracks does not count the pregap "track")
        res = _common.open_and_parse_test_data(self.datadir, "f7agNZK1HMQ2WUWq9bwDymw9aHA-.xml")
        self.assertEqual(res["disc"]["offset-count"], 13)

    def testOffsets(self):
        """
        Test that the correct list of offsets is returned.
        """
        res = _common.open_and_parse_test_data(self.datadir, "xp5tz6rE4OHrBafj0bLfDRMGK48-.xml")
        offsets_res = res["disc"]["offset-list"]
        offsets_correct = [182, 33322, 52597, 73510, 98882, 136180, 169185, 187490]
        for i in range(len(offsets_correct)):
            self.assertEqual(offsets_res[i], offsets_correct[i])
            self.assertTrue(isinstance(offsets_res[i], int))

    def testReleaseList(self):
        """
        Test that a release list of correct size is given.
        """
        res = _common.open_and_parse_test_data(self.datadir, "xp5tz6rE4OHrBafj0bLfDRMGK48-.xml")
        self.assertEqual(res["disc"]["release-count"], 3)
        self.assertEqual(res["disc"]["release-count"], len(res["disc"]["release-list"]))
