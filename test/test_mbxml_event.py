# Tests for parsing of event queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from test import _common


class GetEventTest(unittest.TestCase):

    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "event")

    def testCorrectId(self):
        event_id = "770fb0b4-0ad8-4774-9275-099b66627355"
        res = _common.open_and_parse_test_data(self.datadir, "%s-place-rels.xml" % event_id)
        self.assertEqual(event_id, res["event"]["id"])
