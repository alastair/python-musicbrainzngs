# Tests for parsing of place results

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from test import _common


class PlaceTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "place")

    def testPlace(self):
        filename = "0c79cdbb-acd6-4e30-aaa3-a5c8d6b36a48-aliases-tags.xml"
        res = _common.open_and_parse_test_data(self.datadir, filename)

        p = res["place"]
        self.assertEquals("All Saints' Church", p["name"])
        self.assertEquals("East Finchley, Durham Road", p["disambiguation"])
        self.assertEquals("38 Durham Road, London N2 9DP, United Kingdom", p["address"])
        self.assertEquals({"latitude": "51.591812", "longitude": "-0.159699"}, p["coordinates"])
        self.assertEquals("f03d09b3-39dc-4083-afd6-159e3f0d462f", p["area"]["id"])
        self.assertEquals("1891", p["life-span"]["begin"])
        self.assertEquals("All Saints' Durham Road", p["alias-list"][0]["alias"])
        self.assertEquals("type=church", p["tag-list"][0]["name"])
        self.assertEquals("1", p["tag-list"][0]["count"])

    def testListFromBrowse(self):
        filename = "browse-area-74e50e58-5deb-4b99-93a2-decbb365c07f-annotation.xml"
        res = _common.open_and_parse_test_data(self.datadir, filename)

        self.assertEqual(395, res["place-count"])
        self.assertEqual(25, len(res["place-list"]))

        self.assertTrue(res["place-list"][13]["annotation"]["text"].startswith("was later renamed"))

