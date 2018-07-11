# coding=utf-8
# Tests for parsing of work queries

import unittest
import os
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


        res = _common.open_and_parse_test_data(self.datadir, "3d7c7cd2-da79-37f4-98b8-ccfb1a4ac6c4-aliases.xml")
        aliases = res["work"]["alias-list"]
        self.assertEqual(len(aliases), 10)

        a0 = aliases[0]
        self.assertEqual(a0["alias"], "Adagio from Symphony No. 2 in E minor, Op. 27")
        self.assertEqual(a0["sort-name"], "Adagio from Symphony No. 2 in E minor, Op. 27")

    def testWorkAttributes(self):
        res = _common.open_and_parse_test_data(self.datadir, "80737426-8ef3-3a9c-a3a6-9507afb93e93-aliases.xml")
        work_attrs = res["work"]["attribute-list"]
        self.assertEqual(len(work_attrs), 1)
        attr = work_attrs[0]

        expected = {"attribute": "Key", "value": "E-flat major"}
        self.assertEqual(expected, attr)

        res = _common.open_and_parse_test_data(self.datadir, "8e134b32-99b8-4e96-ae5c-426f3be85f4c-attributes.xml")
        work_attrs = res["work"]["attribute-list"]
        self.assertEqual(len(work_attrs), 3)
        expected = {"attribute": "Makam (Ottoman, Turkish)", "value": b"H\xc3\xbczzam".decode("utf-8")}
        self.assertEqual(expected, work_attrs[0])
        expected = {"attribute": "Form (Ottoman, Turkish)", "value": b"Pe\xc5\x9frev".decode("utf-8")}
        self.assertEqual(expected, work_attrs[1])
        expected = {"attribute": "Usul (Ottoman, Turkish)", "value": "Fahte"}
        self.assertEqual(expected, work_attrs[2])

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
        expected = {"attribute": "number", "value": "BuxWV 1"}
        self.assertEqual(expected, attributes[0])
