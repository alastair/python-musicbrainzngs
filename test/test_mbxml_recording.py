# coding=utf-8
# Tests for parsing of recording queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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
        attributes = rels[2]["attribute-list"]
        self.assertEqual("piano", attributes[0])

        # New attribute dict format
        attributes = rels[2]["attributes"]
        self.assertEqual("piano", attributes[0]["attribute"])
        self.assertEqual("Yamaha and Steinway pianos", attributes[0]["credited-as"])
