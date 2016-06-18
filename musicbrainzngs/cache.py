import hashlib


class NotInCache(Exception):
    pass


class BaseCache(object):
    def get(self, key, url, args, method):
        raise NotImplementedError

    def set(self, key, value, url, args, method):
        raise NotImplementedError

    def build_key(self, url, args, method):
        """Since the URL contains all the arguments, we can build
        the cache key by simply hashing the url"""
        return hashlib.sha1(url.encode('utf-8')).hexdigest()


class DictCache(BaseCache):
    """A really basic implementation of a cache that will store
    the cached values in a dictionary"""

    def __init__(self):
        self._cache = {}

    def get(self, key, url, args, method):
        try:
            return self._cache[key]
        except KeyError:
            raise NotInCache(key)

    def set(self, key, value, url, args, method):
        self._cache[key] = value


def _get_from_cache(cache_obj, url, args, method):
    if not cache_obj:
        #  no cache is configured, just return
        raise NotInCache('Cache is not configured')

    if method != 'GET':
        # we don't want to cache respons for requests that modify data
        raise NotInCache('{0} method is not cachable'.format(method))

    cache_key = cache_obj.build_key(url=url, args=args, method=method)
    return cache_obj.get(key=cache_key, url=url, args=args, method=method)


def _set_cache(cache_obj, resp, url, args, method):
    if not cache_obj:
        #  no cache is configured, just return
        return

    if method != 'GET':
        # we don't want to cache respons for requests that modify data
        return

    cache_key = cache_obj.build_key(url=url, args=args, method=method)
    return cache_obj.set(key=cache_key, value=resp, url=url, args=args, method=method)
