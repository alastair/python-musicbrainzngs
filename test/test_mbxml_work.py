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
        self.assertEqual(len(aliases), 3)

        a0 = aliases[0]
        self.assertEqual(a0["alias"], u'Sinfonia nro 3 Es-duuri, op. 55 ”Eroica”')
        self.assertEqual(a0["sort-name"], u'Sinfonia nro 3 Es-duuri, op. 55 ”Eroica”')

        a1 = aliases[2]
        self.assertEqual(a1["alias"], 'Symphony No. 3, Op. 55 "Eroica"')
        self.assertEqual(a1["sort-name"], 'Symphony No. 3, Op. 55 "Eroica"')

        res = _common.open_and_parse_test_data(self.datadir, "3d7c7cd2-da79-37f4-98b8-ccfb1a4ac6c4-aliases.xml")
        aliases = res["work"]["alias-list"]
        self.assertEqual(len(aliases), 11)

        a0 = aliases[0]
        self.assertEqual(a0["alias"], "Adagio from Symphony No. 2 in E minor, Op. 27")
        self.assertEqual(a0["sort-name"], "Adagio from Symphony No. 2 in E minor, Op. 27")

    def testWorkAttributes(self):
        res = _common.open_and_parse_test_data(self.datadir, "80737426-8ef3-3a9c-a3a6-9507afb93e93-aliases.xml")
        work_attrs = res["work"]["attribute-list"]
        self.assertEqual(len(work_attrs), 1)
        attr = work_attrs[0]

        expected = {"attribute": "Key",
                    "type": "Key",
                    "type-id": "7526c19d-3be4-3420-b6cc-9fb6e49fa1a9",
                    "value": "E-flat major",
                    "value-id": "7ed963d7-dba9-3357-aefa-f34accb047cd"}
        self.assertEqual(expected, attr)

        res = _common.open_and_parse_test_data(self.datadir, "8e134b32-99b8-4e96-ae5c-426f3be85f4c-attributes.xml")
        work_attrs = res["work"]["attribute-list"]
        self.assertEqual(len(work_attrs), 3)
        expected = {"type": "Makam (Ottoman, Turkish)",
                    "attribute": "Makam (Ottoman, Turkish)",
                    "value": b"H\xc3\xbczzam".decode("utf-8"),
                    "type-id": "d7979776-ba34-3e8d-980f-4849b38143d2",
                    "value-id": "583b64cf-bc36-3dae-8b1d-f834e0a7d9f6"}
        self.assertEqual(expected, work_attrs[0])
        expected = {"type": "Form (Ottoman, Turkish)",
                    "attribute": "Form (Ottoman, Turkish)",
                    "value": b"Pe\xc5\x9frev".decode("utf-8"),
                    "type-id": "77d00f78-0b30-3d91-80de-209a014d33a2",
                    "value-id": "e2d21124-9c1f-3091-b8cc-b49714a84c8b"}
        self.assertEqual(expected, work_attrs[1])
        expected = {"type": "Usul (Ottoman, Turkish)",
                    "attribute": "Usul (Ottoman, Turkish)",
                    "value": "Fahte",
                    "type-id": "29a16dc2-8602-3fee-9a03-a8cc87fa961d",
                    "value-id": "70636c0a-30da-310c-a7e8-c1113f35dab8"}
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
        expected = {"attribute": "number", "value": "BuxWV 1", "type-id": "a59c5830-5ec7-38fe-9a21-c7ea54f6650a"}
        self.assertEqual(expected, attributes[0])
