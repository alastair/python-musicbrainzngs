# Tests for parsing of release queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from musicbrainzngs import mbxml


class GetReleaseGroupTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data",
                "release-group")

    def testTypesExist(self):
        fn = os.path.join(self.datadir,
                          "f52bc6a1-c848-49e6-85de-f8f53459a624.xml")
        res = mbxml.parse_message(open(fn))["release-group"]
        self.assertTrue("type" in res)
        self.assertTrue("primary-type" in res)
        self.assertTrue("secondary-type-list" in res)

    def testTypesResult(self):
        fn = os.path.join(self.datadir,
                          "f52bc6a1-c848-49e6-85de-f8f53459a624.xml")
        res = mbxml.parse_message(open(fn))["release-group"]
        self.assertEqual("Soundtrack", res["type"])
        self.assertEqual("Album", res["primary-type"])
        self.assertEqual(["Soundtrack"], res["secondary-type-list"])
