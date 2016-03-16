# coding=utf-8
# Tests for parsing of work queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from test import _common

class GetWorkTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "work")

    def testWorkAliases(self):
        res = _common.open_and_parse_test_data(self.datadir, "80737426-8ef3-3a9c-a3a6-9507afb93e93-aliases.xml")
        aliases = res["work"]["alias-list"]
        self.assertEqual(len(aliases), 2)

        a0 = aliases[0]
        self.assertEqual(a0["alias"], 'Symphonie Nr. 3 Es-Dur, Op. 55 "Eroica"')
        self.assertEqual(a0["sort-name"], 'Symphonie Nr. 3 Es-Dur, Op. 55 "Eroica"')

        a1 = aliases[1]
        self.assertEqual(a1["alias"], 'Symphony No. 3, Op. 55 "Eroica"')
        self.assertEqual(a1["sort-name"], 'Symphony No. 3, Op. 55 "Eroica"')

        work_attrs = res["work"]["attribute-list"]
        self.assertEqual(len(work_attrs), 1)
        attr = work_attrs[0]
        self.assertEqual(attr["type"], "Key")
        self.assertEqual(attr["attribute"], "E-flat major")

        res = _common.open_and_parse_test_data(self.datadir, "3d7c7cd2-da79-37f4-98b8-ccfb1a4ac6c4-aliases.xml")
        aliases = res["work"]["alias-list"]
        self.assertEqual(len(aliases), 10)

        a0 = aliases[0]
        self.assertEqual(a0["alias"], "Adagio from Symphony No. 2 in E minor, Op. 27")
        self.assertEqual(a0["sort-name"], "Adagio from Symphony No. 2 in E minor, Op. 27")

    def testWorkRelationAttributes(self):
        # Some relation attributes can contain attributes as well as text
        res = _common.open_and_parse_test_data(self.datadir, "72c9aad2-3c95-4e3e-8a01-3974f8fef8eb-series-rels.xml")

        work = res["work"]
        rels = work["series-relation-list"]

        self.assertEqual(1, len(rels))
        # Original attributes
        attributes = rels[0]["attribute-list"]
        self.assertEqual("number", attributes[0])

        # New attribute dict format
        attributes = rels[0]["attributes"]
        self.assertEqual("number", attributes[0]["attribute"])
        self.assertEqual("BuxWV 1", attributes[0]["value"])
