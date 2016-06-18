import unittest
import mock
import hashlib
import musicbrainzngs.cache


class DummyCache(musicbrainzngs.cache.BaseCache):
    pass


class CacheTest(unittest.TestCase):
    """ Test that we can cache results"""

    def setUp(self):
        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)
        self.cache = musicbrainzngs.cache.BaseCache()
        musicbrainzngs.set_cache(self.cache)

    def tearDown(self):
        musicbrainzngs.set_cache(None)
        
    @mock.patch('musicbrainzngs.musicbrainz._safe_read', return_value='return_value')
    @mock.patch('musicbrainzngs.musicbrainz.parser_fun')
    @mock.patch('musicbrainzngs.cache.BaseCache.get', side_effect=musicbrainzngs.cache.NotInCache)
    def test_cache_is_set_after_mb_request(self, *mocks):
        """ Check the cache is called when set on the client"""
        expected_kwargs = {
            'args': [],
            'method': 'GET',
            'url': 'http://musicbrainz.org/ws/2/artist/mbid',
        }
        expected_kwargs['key'] = self.cache.build_key(**expected_kwargs)
        h = hashlib.sha1(expected_kwargs['url'].encode('utf-8')).hexdigest()

        self.assertEqual(expected_kwargs['key'], h)

        with mock.patch('musicbrainzngs.cache.BaseCache.set') as cache:
            musicbrainzngs.get_artist_by_id('mbid')
            cache.assert_called_once_with(value='return_value', **expected_kwargs)

    @mock.patch('musicbrainzngs.musicbrainz.parser_fun', side_effect=lambda v: v)
    @mock.patch('musicbrainzngs.cache.BaseCache.set')
    def test_cache_get_is_called_before_request(self, *mocks):
        expected_kwargs = {
            'args': [],
            'method': 'GET',
            'url': 'http://musicbrainz.org/ws/2/artist/mbid',
        }

        expected_kwargs['key'] = self.cache.build_key(**expected_kwargs)
        h = hashlib.sha1(expected_kwargs['url'].encode('utf-8')).hexdigest()

        self.assertEqual(expected_kwargs['key'], h)

        with mock.patch('musicbrainzngs.cache.BaseCache.get', return_value='value') as cache:
            r = musicbrainzngs.get_artist_by_id('mbid')
            cache.assert_called_once_with(**expected_kwargs)
            self.assertEqual(r, 'value')
