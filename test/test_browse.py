import musicbrainzngs
from test import _common
from re import compile


class BrowseTest(_common.RequestsMockingTestCase):
    def setUp(self):
        super(BrowseTest, self).setUp()

        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)
        self.m.get(compile("ws/2/.*/\?.*"), text="<response/>")

    def tearDown(self):
        musicbrainzngs.set_rate_limit(True)

    def test_browse(self):
        area = "74e50e58-5deb-4b99-93a2-decbb365c07f"
        musicbrainzngs.browse_events(area=area)
        self.assertEqual("https://musicbrainz.org/ws/2/event/?area=74e50e58-5deb-4b99-93a2-decbb365c07f", self.last_url)

    def test_browse_includes(self):
        area = "74e50e58-5deb-4b99-93a2-decbb365c07f"
        musicbrainzngs.browse_events(area=area, includes=["aliases", "area-rels"])
        self.assertEqual("https://musicbrainz.org/ws/2/event/?area=74e50e58-5deb-4b99-93a2-decbb365c07f&inc=aliases+area-rels", self.last_url)

    def test_browse_single_include(self):
        area = "74e50e58-5deb-4b99-93a2-decbb365c07f"
        musicbrainzngs.browse_events(area=area, includes="aliases")
        self.assertEqual("https://musicbrainz.org/ws/2/event/?area=74e50e58-5deb-4b99-93a2-decbb365c07f&inc=aliases", self.last_url)

    def test_browse_multiple_by(self):
        """It is an error to choose multiple entities to browse by"""
        self.assertRaises(Exception,
                musicbrainzngs.browse_artists, recording="1", release="2")

    def test_browse_limit_offset(self):
        """Limit and offset values"""
        area = "74e50e58-5deb-4b99-93a2-decbb365c07f"
        musicbrainzngs.browse_events(area=area, limit=50, offset=100)
        self.assertEqual("https://musicbrainz.org/ws/2/event/?area=74e50e58-5deb-4b99-93a2-decbb365c07f&limit=50&offset=100", self.last_url)

    def test_browse_artist(self):
        release = "9ace7c8c-55b4-4c5d-9aa8-e573a5dde9ad"
        musicbrainzngs.browse_artists(release=release)
        self.assertEqual("https://musicbrainz.org/ws/2/artist/?release=9ace7c8c-55b4-4c5d-9aa8-e573a5dde9ad", self.last_url)

        recording = "6da2cc31-9b12-4b66-9e26-074150f73406"
        musicbrainzngs.browse_artists(recording=recording)
        self.assertEqual("https://musicbrainz.org/ws/2/artist/?recording=6da2cc31-9b12-4b66-9e26-074150f73406", self.last_url)

        release_group = "44c90c72-76b5-3c13-890e-3d37f21c10c9"
        musicbrainzngs.browse_artists(release_group=release_group)
        self.assertEqual("https://musicbrainz.org/ws/2/artist/?release-group=44c90c72-76b5-3c13-890e-3d37f21c10c9", self.last_url)

        work = "deb27b88-cf41-4f7c-b3aa-bc3268bc3c02"
        musicbrainzngs.browse_artists(work=work)
        self.assertEqual("https://musicbrainz.org/ws/2/artist/?work=deb27b88-cf41-4f7c-b3aa-bc3268bc3c02", self.last_url)

    def test_browse_event(self):
        area = "f03d09b3-39dc-4083-afd6-159e3f0d462f"
        musicbrainzngs.browse_events(area=area)
        self.assertEqual("https://musicbrainz.org/ws/2/event/?area=f03d09b3-39dc-4083-afd6-159e3f0d462f", self.last_url)

        artist = "0383dadf-2a4e-4d10-a46a-e9e041da8eb3"
        musicbrainzngs.browse_events(artist=artist)
        self.assertEqual("https://musicbrainz.org/ws/2/event/?artist=0383dadf-2a4e-4d10-a46a-e9e041da8eb3", self.last_url)

        place = "8a6161bb-fb50-4234-82c5-1e24ab342499"
        musicbrainzngs.browse_events(place=place)
        self.assertEqual("https://musicbrainz.org/ws/2/event/?place=8a6161bb-fb50-4234-82c5-1e24ab342499", self.last_url)

    def test_browse_label(self):
        release = "c9550260-b7ae-4670-ac24-731c19e76b59"
        musicbrainzngs.browse_labels(release=release)
        self.assertEqual("https://musicbrainz.org/ws/2/label/?release=c9550260-b7ae-4670-ac24-731c19e76b59", self.last_url)

    def test_browse_recording(self):
        artist = "47f67b22-affe-4fe1-9d25-853d69bc0ee3"
        musicbrainzngs.browse_recordings(artist=artist)
        self.assertEqual("https://musicbrainz.org/ws/2/recording/?artist=47f67b22-affe-4fe1-9d25-853d69bc0ee3", self.last_url)

        release = "438042ef-7ccc-4d03-9391-4f66427b2055"
        musicbrainzngs.browse_recordings(release=release)
        self.assertEqual("https://musicbrainz.org/ws/2/recording/?release=438042ef-7ccc-4d03-9391-4f66427b2055", self.last_url)

    def test_browse_place(self):
        area = "74e50e58-5deb-4b99-93a2-decbb365c07f"
        musicbrainzngs.browse_places(area=area)
        self.assertEqual("https://musicbrainz.org/ws/2/place/?area=74e50e58-5deb-4b99-93a2-decbb365c07f", self.last_url)

    def test_browse_release(self):
        artist = "47f67b22-affe-4fe1-9d25-853d69bc0ee3"
        musicbrainzngs.browse_releases(artist=artist)
        self.assertEqual("https://musicbrainz.org/ws/2/release/?artist=47f67b22-affe-4fe1-9d25-853d69bc0ee3", self.last_url)
        musicbrainzngs.browse_releases(track_artist=artist)
        self.assertEqual("https://musicbrainz.org/ws/2/release/?track_artist=47f67b22-affe-4fe1-9d25-853d69bc0ee3", self.last_url)

        label = "713c4a95-6616-442b-9cf6-14e1ddfd5946"
        musicbrainzngs.browse_releases(label=label)
        self.assertEqual("https://musicbrainz.org/ws/2/release/?label=713c4a95-6616-442b-9cf6-14e1ddfd5946", self.last_url)

        recording = "7484fcfd-1968-4401-a44d-d1edcc580518"
        musicbrainzngs.browse_releases(recording=recording)
        self.assertEqual("https://musicbrainz.org/ws/2/release/?recording=7484fcfd-1968-4401-a44d-d1edcc580518", self.last_url)

        release_group = "1c1b54f7-e56a-3ce8-b62c-e45c378e7f76"
        musicbrainzngs.browse_releases(release_group=release_group)
        self.assertEqual("https://musicbrainz.org/ws/2/release/?release-group=1c1b54f7-e56a-3ce8-b62c-e45c378e7f76", self.last_url)

    def test_browse_release_group(self):
        artist = "47f67b22-affe-4fe1-9d25-853d69bc0ee3"
        musicbrainzngs.browse_release_groups(artist=artist)
        self.assertEqual("https://musicbrainz.org/ws/2/release-group/?artist=47f67b22-affe-4fe1-9d25-853d69bc0ee3", self.last_url)

        release = "438042ef-7ccc-4d03-9391-4f66427b2055"
        musicbrainzngs.browse_release_groups(release=release)
        self.assertEqual("https://musicbrainz.org/ws/2/release-group/?release=438042ef-7ccc-4d03-9391-4f66427b2055", self.last_url)

        release = "438042ef-7ccc-4d03-9391-4f66427b2055"
        rel_type = "ep"
        musicbrainzngs.browse_release_groups(release=release, release_type=rel_type)
        self.assertEqual("https://musicbrainz.org/ws/2/release-group/?release=438042ef-7ccc-4d03-9391-4f66427b2055&type=ep", self.last_url)

    def test_browse_url(self):
        resource = "http://www.queenonline.com"
        musicbrainzngs.browse_urls(resource=resource)
        self.assertEqual("https://musicbrainz.org/ws/2/url/?resource=http%3A%2F%2Fwww.queenonline.com", self.last_url)

        # Resource is urlencoded, including ? and =
        resource = "http://www.splendidezine.com/review.html?reviewid=1109588405202831"
        musicbrainzngs.browse_urls(resource=resource)
        self.assertEqual("https://musicbrainz.org/ws/2/url/?resource=http%3A%2F%2Fwww.splendidezine.com%2Freview.html%3Freviewid%3D1109588405202831", self.last_url)

    def test_browse_work(self):
        artist = "0383dadf-2a4e-4d10-a46a-e9e041da8eb3"
        musicbrainzngs.browse_works(artist=artist)
        self.assertEqual("https://musicbrainz.org/ws/2/work/?artist=0383dadf-2a4e-4d10-a46a-e9e041da8eb3", self.last_url)

    def test_browse_includes_is_subset_of_includes(self):
        """Check that VALID_BROWSE_INCLUDES is a strict subset of
           VALID_INCLUDES"""
        for entity, includes in musicbrainzngs.VALID_BROWSE_INCLUDES.items():
            for i in includes:
                self.assertTrue(i in musicbrainzngs.VALID_INCLUDES[entity], "entity %s, %s in BROWSE_INCLUDES but not VALID_INCLUDES" % (entity, i))
