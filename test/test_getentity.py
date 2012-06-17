import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import musicbrainzngs
from test import _common


class UrlTest(unittest.TestCase):
    """ Test that the correct URL is generated when a search query is made """

    def setUp(self):
        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)

    def testGetArtist(self):
        artistid = "952a4205-023d-4235-897c-6fdb6f58dfaa"
        musicbrainzngs.get_artist_by_id(artistid)
        self.assertEqual("http://musicbrainz.org/ws/2/artist/952a4205-023d-4235-897c-6fdb6f58dfaa", _common.opener.get_url())

        # Test an include
        musicbrainzngs.get_artist_by_id(artistid, "recordings")
        self.assertEqual("http://musicbrainz.org/ws/2/artist/952a4205-023d-4235-897c-6fdb6f58dfaa?inc=recordings", _common.opener.get_url())

        # More than one include
        musicbrainzngs.get_artist_by_id(artistid, ["recordings", "aliases"])
        expected ="http://musicbrainz.org/ws/2/artist/952a4205-023d-4235-897c-6fdb6f58dfaa?inc=recordings+aliases"
        self.assertEqual(expected, _common.opener.get_url())

    def testGetLabel(self):
        musicbrainzngs.get_label_by_id("aab2e720-bdd2-4565-afc2-460743585f16")
        self.assertEqual("http://musicbrainz.org/ws/2/label/aab2e720-bdd2-4565-afc2-460743585f16", _common.opener.get_url())

        # one include
        musicbrainzngs.get_label_by_id("aab2e720-bdd2-4565-afc2-460743585f16", "releases")
        self.assertEqual("http://musicbrainz.org/ws/2/label/aab2e720-bdd2-4565-afc2-460743585f16?inc=releases", _common.opener.get_url())

    def testGetRecording(self):
        musicbrainzngs.get_recording_by_id("93468a09-9662-4886-a227-56a2ad1c5246")
        self.assertEqual("http://musicbrainz.org/ws/2/recording/93468a09-9662-4886-a227-56a2ad1c5246", _common.opener.get_url())

        # one include
        musicbrainzngs.get_recording_by_id("93468a09-9662-4886-a227-56a2ad1c5246", includes=["artists"])
        self.assertEqual("http://musicbrainz.org/ws/2/recording/93468a09-9662-4886-a227-56a2ad1c5246?inc=artists", _common.opener.get_url())


    def testGetReleasegroup(self):
        musicbrainzngs.get_release_group_by_id("9377d65d-ffd5-35d6-b64d-43f86ef9188d")
        self.assertEqual("http://musicbrainz.org/ws/2/release-group/9377d65d-ffd5-35d6-b64d-43f86ef9188d", _common.opener.get_url())

        # one include
        musicbrainzngs.get_release_group_by_id("9377d65d-ffd5-35d6-b64d-43f86ef9188d", includes=["artists"])
        self.assertEqual("http://musicbrainz.org/ws/2/release-group/9377d65d-ffd5-35d6-b64d-43f86ef9188d?inc=artists", _common.opener.get_url())

    def testGetWork(self):
        musicbrainzngs.get_work_by_id("c6dfad5a-f915-41c7-a1c0-e2b606948e69")
        self.assertEqual("http://musicbrainz.org/ws/2/work/c6dfad5a-f915-41c7-a1c0-e2b606948e69", _common.opener.get_url())

