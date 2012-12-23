# coding=utf-8
# Tests for parsing of work queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import musicbrainzngs
from musicbrainzngs import mbxml

class GetWorkTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "work")

    def testWorkAliases(self):
        fn = os.path.join(self.datadir, "80737426-8ef3-3a9c-a3a6-9507afb93e93-aliases.xml")
        res = mbxml.parse_message(open(fn))
        aliases = res["work"]["alias-list"]
        self.assertEqual(len(aliases), 2)

        a0 = aliases[0]
        self.assertEqual(a0["alias"], 'Symphonie Nr. 3 Es-Dur, Op. 55 "Eroica"')
        self.assertEqual(a0["sort-name"], 'Symphonie Nr. 3 Es-Dur, Op. 55 "Eroica"')

        a1 = aliases[1]
        self.assertEqual(a1["alias"], 'Symphony No. 3, Op. 55 "Eroica"')
        self.assertEqual(a1["sort-name"], 'Symphony No. 3, Op. 55 "Eroica"')

        fn = os.path.join(self.datadir, "3d7c7cd2-da79-37f4-98b8-ccfb1a4ac6c4-aliases.xml")
        res = mbxml.parse_message(open(fn))
        aliases = res["work"]["alias-list"]
        self.assertEqual(len(aliases), 10)

        a0 = aliases[0]
        self.assertEqual(a0["alias"], "Adagio from Symphony No. 2 in E minor, Op. 27")
        self.assertEqual(a0["sort-name"], "Adagio from Symphony No. 2 in E minor, Op. 27")

