# Tests for parsing of collection queries

import unittest
import os
import musicbrainzngs
from test import _common
from re import compile


class UrlTest(_common.RequestsMockingTestCase):
    """ Test that the correct URL is generated when a query is made """

    def setUp(self):
        super(UrlTest, self).setUp()

        musicbrainzngs.set_useragent("test", "1")
        musicbrainzngs.set_rate_limit(False)

        self.m.get(compile("ws/2/.*/.*"), text="<response/>")

    def tearDown(self):
        musicbrainzngs.set_rate_limit(True)

    def testGetCollection(self):
        musicbrainzngs.get_releases_in_collection("0b15c97c-8eb8-4b4f-81c3-0eb24266a2ac")
        self.assertEqual("https://musicbrainz.org/ws/2/collection/0b15c97c-8eb8-4b4f-81c3-0eb24266a2ac/releases", self.last_url)

        musicbrainzngs.get_works_in_collection("898676a6-bc79-4fe2-98ae-79c5940fe1a2")
        self.assertEqual("https://musicbrainz.org/ws/2/collection/898676a6-bc79-4fe2-98ae-79c5940fe1a2/works", self.last_url)

        musicbrainzngs.get_events_in_collection("65cb5dda-44aa-44a8-9c0d-4f99a14ab944")
        self.assertEqual("https://musicbrainz.org/ws/2/collection/65cb5dda-44aa-44a8-9c0d-4f99a14ab944/events", self.last_url)

        musicbrainzngs.get_places_in_collection("9dde4c3c-520a-4bfd-9aae-446c3a04ce0c")
        self.assertEqual("https://musicbrainz.org/ws/2/collection/9dde4c3c-520a-4bfd-9aae-446c3a04ce0c/places", self.last_url)

        musicbrainzngs.get_recordings_in_collection("42bc6dd9-8deb-4bd7-83eb-5dacdb218b38")
        self.assertEqual("https://musicbrainz.org/ws/2/collection/42bc6dd9-8deb-4bd7-83eb-5dacdb218b38/recordings", self.last_url)

        musicbrainzngs.get_artists_in_collection("7e582256-b3ce-421f-82ba-451b0ab080eb")
        self.assertEqual("https://musicbrainz.org/ws/2/collection/7e582256-b3ce-421f-82ba-451b0ab080eb/artists", self.last_url)


class GetCollectionTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "collection")

    def testCollectionInfo(self):
        """
        Test that the id, name and author are given.
        """
        res = _common.open_and_parse_test_data(self.datadir, "0b15c97c-8eb8-4b4f-81c3-0eb24266a2ac-releases.xml")

    def testCollectionReleases(self):
        """
        Test that the list of releases is given.
        """
        res = _common.open_and_parse_test_data(self.datadir, "0b15c97c-8eb8-4b4f-81c3-0eb24266a2ac-releases.xml")
        coll = res["collection"]
        self.assertEqual(coll["id"], "0b15c97c-8eb8-4b4f-81c3-0eb24266a2ac")
        self.assertEqual(coll["name"], "My Collection")
        self.assertEqual(coll["editor"], "JonnyJD")
        self.assertEqual(coll["entity-type"], "release")
        self.assertEqual(coll["type"], "Release")
        self.assertEqual(coll["release-count"], 400)
        self.assertTrue("release-list" in res["collection"])

    def testCollectionWorks(self):
        res = _common.open_and_parse_test_data(self.datadir, "2326c2e8-be4b-4300-acc6-dbd0adf5645b-works.xml")
        coll = res["collection"]
        self.assertEqual(coll["id"], "2326c2e8-be4b-4300-acc6-dbd0adf5645b")
        self.assertEqual(coll["name"], "work collection")
        self.assertEqual(coll["editor"], "alastairp")
        self.assertEqual(coll["entity-type"], "work")
        self.assertEqual(coll["type"], "Work")
        self.assertEqual(coll["work-count"], 1)
        self.assertEqual(len(coll["work-list"]), 1)

    def testCollectionArtists(self):
        res = _common.open_and_parse_test_data(self.datadir, "29611d8b-b3ad-4ffb-acb5-27f77342a5b0-artists.xml")
        coll = res["collection"]
        self.assertEqual(coll["id"], "29611d8b-b3ad-4ffb-acb5-27f77342a5b0")
        self.assertEqual(coll["name"], "artist collection")
        self.assertEqual(coll["editor"], "alastairp")
        self.assertEqual(coll["entity-type"], "artist")
        self.assertEqual(coll["type"], "Artist")
        self.assertEqual(coll["artist-count"], 1)
        self.assertEqual(len(coll["artist-list"]), 1)

    def testCollectionEvents(self):
        res = _common.open_and_parse_test_data(self.datadir, "20562e36-c7cc-44fb-96b4-486d51a1174b-events.xml")
        coll = res["collection"]
        self.assertEqual(coll["id"], "20562e36-c7cc-44fb-96b4-486d51a1174b")
        self.assertEqual(coll["name"], "event collection")
        self.assertEqual(coll["editor"], "alastairp")
        self.assertEqual(coll["entity-type"], "event")
        self.assertEqual(coll["type"], "Event")
        self.assertEqual(coll["event-count"], 1)
        self.assertEqual(len(coll["event-list"]), 1)

    def testCollectionPlaces(self):
        res = _common.open_and_parse_test_data(self.datadir, "855b134e-9a3b-4717-8df8-8c4838d89924-places.xml")
        coll = res["collection"]
        self.assertEqual(coll["id"], "855b134e-9a3b-4717-8df8-8c4838d89924")
        self.assertEqual(coll["name"], "place collection")
        self.assertEqual(coll["editor"], "alastairp")
        self.assertEqual(coll["entity-type"], "place")
        self.assertEqual(coll["type"], "Place")
        self.assertEqual(coll["place-count"], 1)
        self.assertEqual(len(coll["place-list"]), 1)

    def testCollectionRecordings(self):
        res = _common.open_and_parse_test_data(self.datadir, "a91320b2-fd2f-4a93-9e4e-603d16d514b6-recordings.xml")
        coll = res["collection"]
        self.assertEqual(coll["id"], "a91320b2-fd2f-4a93-9e4e-603d16d514b6")
        self.assertEqual(coll["name"], "recording collection")
        self.assertEqual(coll["editor"], "alastairp")
        self.assertEqual(coll["entity-type"], "recording")
        self.assertEqual(coll["type"], "Recording")
        self.assertEqual(coll["recording-count"], 1)
        self.assertEqual(len(coll["recording-list"]), 1)
