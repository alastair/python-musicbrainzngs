# Tests for parsing of collection queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import musicbrainzngs
from test import _common


class UrlTest(unittest.TestCase):
    """ Test that the correct URL is generated when a query is made """

    def setUp(self):
        self.opener = _common.FakeOpener("<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener

        musicbrainzngs.set_useragent("test", "1")
        musicbrainzngs.set_rate_limit(False)

    def testGetCollection(self):
        musicbrainzngs.get_releases_in_collection("0b15c97c-8eb8-4b4f-81c3-0eb24266a2ac")
        self.assertEqual("http://musicbrainz.org/ws/2/collection/0b15c97c-8eb8-4b4f-81c3-0eb24266a2ac/releases", self.opener.get_url())
        # TODO: get events_in_collection


class GetCollectionTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "collection")

    def testCollectionType(self):
        """
        Test if the type of the collection is parsed correctly.
        """

        res = _common.open_and_parse_test_data(self.datadir, "0b15c97c-8eb8-4b4f-81c3-0eb24266a2ac-releases.xml")
        self.assertEqual(res["collection"]["entity-type"], "release")
        self.assertEqual(res["collection"]["type"], "Release")
        # TODO: example for Event type

    def testCollectionInfo(self):
        """
        Test that the id, name and author are given.
        """
        res = _common.open_and_parse_test_data(self.datadir, "0b15c97c-8eb8-4b4f-81c3-0eb24266a2ac-releases.xml")
        self.assertEqual(res["collection"]["id"], "0b15c97c-8eb8-4b4f-81c3-0eb24266a2ac")
        self.assertEqual(res["collection"]["name"], "My Collection")
        self.assertEqual(res["collection"]["editor"], "JonnyJD")

    def testCollectionReleases(self):
        """
        Test that the list of releases is given.
        """
        res = _common.open_and_parse_test_data(self.datadir, "0b15c97c-8eb8-4b4f-81c3-0eb24266a2ac-releases.xml")
        self.assertEqual(res["collection"]["release-count"], 400)
        self.assertTrue("release-list" in res["collection"])
