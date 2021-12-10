import musicbrainzngs
from re import compile
from test import _common


class SearchUrlTest(_common.RequestsMockingTestCase):
    """ Test that the correct URL is generated when a search query is made """

    def setUp(self):
        super(SearchUrlTest, self).setUp()

        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)
        self.m.get(compile("ws/2/.*/.*"), text="<response/>")

    def tearDown(self):
        musicbrainzngs.set_rate_limit(True)

    def test_search_annotations(self):
        musicbrainzngs.search_annotations("Pieds")
        self.assertEquals("https://musicbrainz.org/ws/2/annotation/?query=Pieds", self.last_url)

        # Query fields
        musicbrainzngs.search_annotations(entity="bdb24cb5-404b-4f60-bba4-7b730325ae47")
        # TODO: We escape special characters and then urlencode all query parameters, which may
        # not be necessary, but MusicBrainz accepts it and appears to return the same value as without
        expected_query = r'entity:(bdb24cb5\-404b\-4f60\-bba4\-7b730325ae47)'
        expected = 'https://musicbrainz.org/ws/2/annotation/?query=%s' % musicbrainzngs.compat.quote_plus(expected_query)
        self.assertEqual(expected, self.last_url)

        # Invalid query field
        with self.assertRaises(musicbrainzngs.InvalidSearchFieldError):
            musicbrainzngs.search_annotations(foo="value")

    def test_search_artists(self):
        musicbrainzngs.search_artists("Dynamo Go")
        self.assertEqual("https://musicbrainz.org/ws/2/artist/?query=Dynamo+Go", self.last_url)

        musicbrainzngs.search_artists(artist="Dynamo Go")
        expected_query = 'artist:(dynamo go)'
        expected = 'https://musicbrainz.org/ws/2/artist/?query=%s' % musicbrainzngs.compat.quote_plus(expected_query)
        self.assertEqual(expected, self.last_url)

        # Invalid query field
        with self.assertRaises(musicbrainzngs.InvalidSearchFieldError):
            musicbrainzngs.search_artists(foo="value")

    def test_search_events(self):
        musicbrainzngs.search_events("woodstock")
        self.assertEqual("https://musicbrainz.org/ws/2/event/?query=woodstock", self.last_url)

        musicbrainzngs.search_events(event="woodstock")
        expected_query = 'event:(woodstock)'
        expected = 'https://musicbrainz.org/ws/2/event/?query=%s' % musicbrainzngs.compat.quote_plus(expected_query)
        self.assertEqual(expected, self.last_url)

        # Invalid query field
        with self.assertRaises(musicbrainzngs.InvalidSearchFieldError):
            musicbrainzngs.search_events(foo="value")

    def test_search_labels(self):
        musicbrainzngs.search_labels("Waysafe")
        self.assertEqual("https://musicbrainz.org/ws/2/label/?query=Waysafe", self.last_url)

        musicbrainzngs.search_labels(label="Waysafe")
        expected_query = 'label:(waysafe)'
        expected = 'https://musicbrainz.org/ws/2/label/?query=%s' % musicbrainzngs.compat.quote_plus(expected_query)
        self.assertEqual(expected, self.last_url)

        # Invalid query field
        with self.assertRaises(musicbrainzngs.InvalidSearchFieldError):
            musicbrainzngs.search_labels(foo="value")

    def test_search_places(self):
        musicbrainzngs.search_places("Fillmore")
        self.assertEqual("https://musicbrainz.org/ws/2/place/?query=Fillmore", self.last_url)

        musicbrainzngs.search_places(place="Fillmore")
        expected_query = 'place:(fillmore)'
        expected = 'https://musicbrainz.org/ws/2/place/?query=%s' % musicbrainzngs.compat.quote_plus(expected_query)
        self.assertEqual(expected, self.last_url)

        # Invalid query field
        with self.assertRaises(musicbrainzngs.InvalidSearchFieldError):
            musicbrainzngs.search_places(foo="value")

    def test_search_releases(self):
        musicbrainzngs.search_releases("Affordable Pop Music")
        self.assertEqual("https://musicbrainz.org/ws/2/release/?query=Affordable+Pop+Music", self.last_url)

        musicbrainzngs.search_releases(release="Affordable Pop Music")
        expected_query = 'release:(affordable pop music)'
        expected = 'https://musicbrainz.org/ws/2/release/?query=%s' % musicbrainzngs.compat.quote_plus(expected_query)

        # Invalid query field
        with self.assertRaises(musicbrainzngs.InvalidSearchFieldError):
            musicbrainzngs.search_releases(foo="value")

    def test_search_release_groups(self):
        musicbrainzngs.search_release_groups("Affordable Pop Music")
        self.assertEqual("https://musicbrainz.org/ws/2/release-group/?query=Affordable+Pop+Music", self.last_url)

        musicbrainzngs.search_release_groups(releasegroup="Affordable Pop Music")
        expected_query = 'releasegroup:(affordable pop music)'
        expected = 'https://musicbrainz.org/ws/2/release-group/?query=%s' % musicbrainzngs.compat.quote_plus(expected_query)
        self.assertEqual(expected, self.last_url)

        # Invalid query field
        with self.assertRaises(musicbrainzngs.InvalidSearchFieldError):
            musicbrainzngs.search_release_groups(foo="value")

    def test_search_recordings(self):
        musicbrainzngs.search_recordings("Thief of Hearts")
        self.assertEqual("https://musicbrainz.org/ws/2/recording/?query=Thief+of+Hearts", self.last_url)

        musicbrainzngs.search_recordings(recording="Thief of Hearts")
        expected_query = 'recording:(thief of hearts)'
        expected = 'https://musicbrainz.org/ws/2/recording/?query=%s' % musicbrainzngs.compat.quote_plus(expected_query)
        self.assertEqual(expected, self.last_url)

        # Invalid query field
        with self.assertRaises(musicbrainzngs.InvalidSearchFieldError):
            musicbrainzngs.search_recordings(foo="value")

    def test_search_works(self):
        musicbrainzngs.search_works("Fountain City")
        self.assertEqual("https://musicbrainz.org/ws/2/work/?query=Fountain+City", self.last_url)

        musicbrainzngs.search_works(work="Fountain City")
        expected_query = 'work:(fountain city)'
        expected = 'https://musicbrainz.org/ws/2/work/?query=%s' % musicbrainzngs.compat.quote_plus(expected_query)
        self.assertEqual(expected, self.last_url)

        # Invalid query field
        with self.assertRaises(musicbrainzngs.InvalidSearchFieldError):
            musicbrainzngs.search_works(foo="value")
