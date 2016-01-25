import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import musicbrainzngs
from musicbrainzngs import musicbrainz
from test import _common

class BrowseTest(unittest.TestCase):

    def setUp(self):
        self.opener = _common.FakeOpener("<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener

    def test_browse(self):
        area = "74e50e58-5deb-4b99-93a2-decbb365c07f"
        musicbrainzngs.browse_events(area=area)
        self.assertEqual("http://musicbrainz.org/ws/2/event/?area=74e50e58-5deb-4b99-93a2-decbb365c07f", self.opener.get_url())

    def test_browse_includes(self):
        area = "74e50e58-5deb-4b99-93a2-decbb365c07f"
        musicbrainzngs.browse_events(area=area, includes=["aliases", "area-rels"])
        self.assertEqual("http://musicbrainz.org/ws/2/event/?area=74e50e58-5deb-4b99-93a2-decbb365c07f&inc=aliases+area-rels", self.opener.get_url())

    def test_browse_single_include(self):
        area = "74e50e58-5deb-4b99-93a2-decbb365c07f"
        musicbrainzngs.browse_events(area=area, includes="aliases")
        self.assertEqual("http://musicbrainz.org/ws/2/event/?area=74e50e58-5deb-4b99-93a2-decbb365c07f&inc=aliases", self.opener.get_url())

