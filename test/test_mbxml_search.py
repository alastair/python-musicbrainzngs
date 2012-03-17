import unittest
import os
import sys
sys.path.append(os.path.abspath(".."))
import musicbrainzngs
from musicbrainzngs import mbxml

import urllib2
import StringIO


class FakeOpener(urllib2.OpenerDirector):
    """ A URL Opener that saves the URL requested and
    returns a dummy response """
    def open(self, request, body=None):
        self.myurl = request.get_full_url()
        return StringIO.StringIO("<response/>")

    def get_url(self):
        return self.myurl

class UrlTest(unittest.TestCase):
    """ Test that the correct URL is generated when a search query is made """

    def build_opener(self, *args):
        self.opener = FakeOpener()
        return self.opener

    def setUp(self):
        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(1, 100)
        urllib2.build_opener = self.build_opener

    def testSearchArtist(self):
        musicbrainzngs.search_artists("Dynamo Go")
        self.assertEqual("http://musicbrainz.org/ws/2/artist/?query=Dynamo+Go", self.opener.get_url())

    def testSearchWork(self):
        musicbrainzngs.search_works("Fountain City")
        self.assertEqual("http://musicbrainz.org/ws/2/work/?query=Fountain+City", self.opener.get_url())

    def testSearchLabel(self):
        musicbrainzngs.search_labels("Waysafe")
        self.assertEqual("http://musicbrainz.org/ws/2/label/?query=Waysafe", self.opener.get_url())

    def testSearchRelease(self):
        musicbrainzngs.search_releases("Affordable Pop Music")
        self.assertEqual("http://musicbrainz.org/ws/2/release/?query=Affordable+Pop+Music", self.opener.get_url())

    def testSearchReleaseGroup(self):
        musicbrainzngs.search_release_groups("Affordable Pop Music")
        self.assertEqual("http://musicbrainz.org/ws/2/release-group/?query=Affordable+Pop+Music", self.opener.get_url())

    def testSearchRecording(self):
        musicbrainzngs.search_recordings("Thief of Hearts")
        self.assertEqual("http://musicbrainz.org/ws/2/recording/?query=Thief+of+Hearts", self.opener.get_url())

