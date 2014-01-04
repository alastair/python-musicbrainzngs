# Tests for parsing of artist queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from test import _common

class GetArtistTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "artist")

    def testArtistAliases(self):
        res = _common.open_and_parse_test_data(self.datadir, "0e43fe9d-c472-4b62-be9e-55f971a023e1-aliases.xml")
        aliases = res["artist"]["alias-list"]
        self.assertEqual(len(aliases), 28)

        a0 = aliases[0]
        self.assertEqual(a0["alias"], "Prokofief")
        self.assertEqual(a0["sort-name"], "Prokofief")

        a17 = aliases[17]
        self.assertEqual(a17["alias"], "Sergei Sergeyevich Prokofiev")
        self.assertEqual(a17["sort-name"], "Prokofiev, Sergei Sergeyevich")
        self.assertEqual(a17["locale"], "en")
        self.assertEqual(a17["primary"], "primary")

        res = _common.open_and_parse_test_data(self.datadir, "2736bad5-6280-4c8f-92c8-27a5e63bbab2-aliases.xml")
        self.assertFalse("alias-list" in res["artist"])

