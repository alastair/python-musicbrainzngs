# Tests for parsing of event results

import unittest
import os
from test import _common


class EventTest(unittest.TestCase):

    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "event")

    def testCorrectId(self):
        event_id = "770fb0b4-0ad8-4774-9275-099b66627355"
        res = _common.open_and_parse_test_data(self.datadir, "%s-place-rels.xml" % event_id)
        self.assertEqual(event_id, res["event"]["id"])

    def testPlace(self):
        event_id = "770fb0b4-0ad8-4774-9275-099b66627355"
        res = _common.open_and_parse_test_data(self.datadir, "%s-place-rels.xml" % event_id)
        place = res["event"]["place-relation-list"][0]["place"]
        self.assertEqual("7643f13a-dcda-4db4-8196-3ffcc1b99ab7", place["id"])
        self.assertEqual("50.33556", place["coordinates"]["latitude"])
        self.assertEqual("6.9475", place["coordinates"]["longitude"])

    def testType(self):
        event_id = "770fb0b4-0ad8-4774-9275-099b66627355"
        res = _common.open_and_parse_test_data(self.datadir, "%s-place-rels.xml" % event_id)
        self.assertEqual("Concert", res["event"]["type"])

    def testEventElements(self):
        filename = "e921686d-ba86-4122-bc3b-777aec90d231-tags-artist-rels.xml"
        res = _common.open_and_parse_test_data(self.datadir, filename)
        e = res["event"]
        keys = ["name", "life-span", "time", "setlist", "artist-relation-list", "tag-list"]
        for k in keys:
            self.assertTrue(k in e, "key %s in dict" % (k, ))
