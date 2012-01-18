import os
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
sys.path.append(os.path.abspath(".."))
from musicbrainzngs import mbxml

class MbXML(unittest.TestCase):

    def testMakeBarcode(self):
        expected = ('<ns0:metadata xmlns:ns0="http://musicbrainz.org/ns/mmd-2.0#">'
                    '<ns0:release-list><ns0:release ns0:id="trid"><ns0:barcode>12345</ns0:barcode>'
                    '</ns0:release></ns0:release-list></ns0:metadata>')
        xml = mbxml.make_barcode_request({'trid':'12345'})
        self.assertEqual(expected, xml)
