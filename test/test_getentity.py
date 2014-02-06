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
        self.opener = _common.FakeOpener("<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener

        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)

    def testGetArtist(self):
        artistid = "952a4205-023d-4235-897c-6fdb6f58dfaa"
        musicbrainzngs.get_artist_by_id(artistid)
        self.assertEqual("http://musicbrainz.org/ws/2/artist/952a4205-023d-4235-897c-6fdb6f58dfaa", self.opener.get_url())

        # Test an include
        musicbrainzngs.get_artist_by_id(artistid, "recordings")
        self.assertEqual("http://musicbrainz.org/ws/2/artist/952a4205-023d-4235-897c-6fdb6f58dfaa?inc=recordings", self.opener.get_url())

        # More than one include
        musicbrainzngs.get_artist_by_id(artistid, ["recordings", "aliases"])
        expected ="http://musicbrainz.org/ws/2/artist/952a4205-023d-4235-897c-6fdb6f58dfaa?inc=recordings+aliases"
        self.assertEqual(expected, self.opener.get_url())

        # with valid filters
        musicbrainzngs.get_artist_by_id(artistid, ["release-groups"],
                release_type=["album"])
        self.assertTrue("type=album" in self.opener.get_url())

        # with invalid filters
        self.assertRaises(musicbrainzngs.UsageError,
                musicbrainzngs.get_artist_by_id,
                artistid, ["release-groups"], release_status=["official"])

    def testGetLabel(self):
        label_id = "aab2e720-bdd2-4565-afc2-460743585f16"
        musicbrainzngs.get_label_by_id(label_id)
        self.assertEqual("http://musicbrainz.org/ws/2/label/aab2e720-bdd2-4565-afc2-460743585f16", self.opener.get_url())

        # one include
        musicbrainzngs.get_label_by_id(label_id, "releases")
        self.assertEqual("http://musicbrainz.org/ws/2/label/aab2e720-bdd2-4565-afc2-460743585f16?inc=releases", self.opener.get_url())

        # with valid filters
        musicbrainzngs.get_label_by_id(label_id, ["releases"],
                release_type=["ep", "single"], release_status=["official"])
        self.assertTrue("type=ep%7Csingle" in self.opener.get_url())
        self.assertTrue("status=official" in self.opener.get_url())

    def testGetRecording(self):
        musicbrainzngs.get_recording_by_id("93468a09-9662-4886-a227-56a2ad1c5246")
        self.assertEqual("http://musicbrainz.org/ws/2/recording/93468a09-9662-4886-a227-56a2ad1c5246", self.opener.get_url())

        # one include
        musicbrainzngs.get_recording_by_id("93468a09-9662-4886-a227-56a2ad1c5246", includes=["artists"])
        self.assertEqual("http://musicbrainz.org/ws/2/recording/93468a09-9662-4886-a227-56a2ad1c5246?inc=artists", self.opener.get_url())


    def testGetReleasegroup(self):
        musicbrainzngs.get_release_group_by_id("9377d65d-ffd5-35d6-b64d-43f86ef9188d")
        self.assertEqual("http://musicbrainz.org/ws/2/release-group/9377d65d-ffd5-35d6-b64d-43f86ef9188d", self.opener.get_url())

        # one include
        release_group_id = "9377d65d-ffd5-35d6-b64d-43f86ef9188d"
        musicbrainzngs.get_release_group_by_id(release_group_id,
                includes=["artists"])
        self.assertEqual("http://musicbrainz.org/ws/2/release-group/9377d65d-ffd5-35d6-b64d-43f86ef9188d?inc=artists", self.opener.get_url())

        # with valid filters
        musicbrainzngs.get_release_group_by_id(release_group_id,
                release_type=["compilation", "live"])
        self.assertTrue("type=compilation%7Clive" in self.opener.get_url())

        # with invalid filters
        self.assertRaises(musicbrainzngs.UsageError,
                musicbrainzngs.get_release_group_by_id,
                release_group_id, release_status=["official", "promotion"])


    def testGetWork(self):
        musicbrainzngs.get_work_by_id("c6dfad5a-f915-41c7-a1c0-e2b606948e69")
        self.assertEqual("http://musicbrainz.org/ws/2/work/c6dfad5a-f915-41c7-a1c0-e2b606948e69", self.opener.get_url())

    def testGetByDiscid(self):
        musicbrainzngs.get_releases_by_discid("I5l9cCSFccLKFEKS.7wqSZAorPU-")
        self.assertEqual("http://musicbrainz.org/ws/2/discid/I5l9cCSFccLKFEKS.7wqSZAorPU-", self.opener.get_url())

        includes = ["artists"]
        musicbrainzngs.get_releases_by_discid("I5l9cCSFccLKFEKS.7wqSZAorPU-", includes)
        self.assertEqual("http://musicbrainz.org/ws/2/discid/I5l9cCSFccLKFEKS.7wqSZAorPU-?inc=artists", self.opener.get_url())

        musicbrainzngs.get_releases_by_discid("discid", toc="toc")
        self.assertEqual("http://musicbrainz.org/ws/2/discid/discid?toc=toc", self.opener.get_url())

        musicbrainzngs.get_releases_by_discid("discid", toc="toc", cdstubs=False)
        self.assertEqual("http://musicbrainz.org/ws/2/discid/discid?cdstubs=no&toc=toc", self.opener.get_url())


