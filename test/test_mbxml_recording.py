# coding=utf-8
# Tests for parsing of recording queries

import unittest
import os
from test import _common


class GetRecordingTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "recording")

    def testRecordingRelationCreditedAs(self):
        # some performance relations have a "credited-as" attribute
        res = _common.open_and_parse_test_data(self.datadir, "f606f733-c1eb-43f3-93c1-71994ea611e3-artist-rels.xml")

        recording = res["recording"]
        rels = recording["artist-relation-list"]

        self.assertEqual(4, len(rels))
        # Original attributes
        print(rels[0])
        print(rels[1])
        print(rels[2])
        print(rels[3])
        attributes = rels[0]["attribute-list"]
        self.assertEqual("piano", attributes[0])

        # New attribute dict format
        attributes = rels[0]["attributes"]
        expected = {"attribute": "piano",
                    "credited-as": "Yamaha and Steinway pianos",
                    "type-id": "b3eac5f9-7859-4416-ac39-7154e2e8d348"}
        self.assertEqual(expected, attributes[0])

    def testFirstReleaseDate(self):
        res = _common.open_and_parse_test_data(self.datadir, "f606f733-c1eb-43f3-93c1-71994ea611e3-artist-rels.xml")
        self.assertEqual(res["recording"]["first-release-date"], "1984")
