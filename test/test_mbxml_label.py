# Tests for parsing of label queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import musicbrainzngs
from musicbrainzngs import mbxml

class GetLabelTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "label")

    def testLabelAliases(self):
        fn = os.path.join(self.datadir, "022fe361-596c-43a0-8e22-bad712bb9548-aliases.xml")
        res = mbxml.parse_message(open(fn))
        aliases = res["label"]["alias-list"]
        self.assertEqual(len(aliases), 4)

        a0 = aliases[0]
        self.assertEqual(a0["alias"], "EMI")
        self.assertEqual(a0["sort-name"], "EMI")

        a1 = aliases[1]
        self.assertEqual(a1["alias"], "EMI Records (UK)")
        self.assertEqual(a1["sort-name"], "EMI Records (UK)")

        fn = os.path.join(self.datadir, "e72fabf2-74a3-4444-a9a5-316296cbfc8d-aliases.xml")
        res = mbxml.parse_message(open(fn))
        aliases = res["label"]["alias-list"]
        self.assertEqual(len(aliases), 1)

        a0 = aliases[0]
        self.assertEqual(a0["alias"], "Ki/oon Records Inc.")
        self.assertEqual(a0["sort-name"], "Ki/oon Records Inc.")
        self.assertEqual(a0["begin-date"], "2001-10")
        self.assertEqual(a0["end-date"], "2012-04")


