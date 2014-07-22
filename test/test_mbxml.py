import unittest
import os
import sys
sys.path.append(os.path.abspath(".."))
from musicbrainzngs import mbxml

class MbXML(unittest.TestCase):

    def testMakeBarcode(self):
        expected = (b'<ns0:metadata xmlns:ns0="http://musicbrainz.org/ns/mmd-2.0#">'
                    b'<ns0:release-list><ns0:release ns0:id="trid"><ns0:barcode>12345</ns0:barcode>'
                    b'</ns0:release></ns0:release-list></ns0:metadata>')
        xml = mbxml.make_barcode_request({'trid':'12345'})
        self.assertEqual(expected, xml)

    def test_read_error(self):
        error = '<?xml version="1.0" encoding="UTF-8"?><error><text>Invalid mbid.</text><text>For usage, please see: http://musicbrainz.org/development/mmd</text></error>'
        parts = mbxml.get_error_message(error)
        self.assertEqual(2, len(parts))
        self.assertEqual("Invalid mbid.", parts[0])
        self.assertEqual(True, parts[1].startswith("For usage"))
