Cache
~~~~~

For various reasons, you'll probably want to reduce the number of queries you run against the public Musicbrainz API endpoint:

- Since requests are throttled, if you send too much requests in a short time, you may end up with 503 errors
- The public endpoint is sometimes under heavy load and can become unavailable
- The public endpoint is used by a lot of people. Less requests imply a faster service for everybody

In order to reduce the number of queries, you can setup a cache to store the result, avoiding requesting data you already fetched.

The cache workflow is a follows:

1. When requesting the API, if a cache is configured, a cache key is created using the request URL and parameters
2. After the API respond, the result is store in the cache under this key, before being returned
3. Next time you make a request, a lookup will be made in the cache. If the value is cached, it will be returned directly (avoiding an extra HTTP request). If not present, the HTTP request is send normally (and the result will be stored in the cache)


Enabling the cache
------------------

Caching is disabled by default, so you'll need to configure the cache:

.. code-block:: python

    import musicbrainzngs.cache

    cache = musicbrainzngs.cache.DictCache()
    musicbrainzngs.set_cache(cache)

    mbid = 'musicbrainz-artist-id'

    # here, the HTTP request is sent to the Musicbrainz API
    real_result = musicbrainzngs.get_artist_by_id(mbid)

    # then, if we send the same request, the cache will be used instead
    cached_result = musicbrainzngs.get_artist_by_id(mbid)

Creating your own cache
-----------------------

The ``DictCache`` used in the previous example is a really simple cache implementation
built using a Python dictionary. Is will be wiped if you leave the Python process.

In production environment, you'll probably want to use a persistent cache, for example
by storing the data in Redis or Memcached.

To do so, you just need to create your own cache class. Here is a dummy example of such an implementation
for redis:

.. code-block:: python

    # int this example, we use https://pypi.python.org/pypi/redis
    import redis
    import musicbrainzngs.cache

    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


    class RedisCache(musicbrainzngs.cache.BaseCache):

        def __init__(self, prefix='musicbrainz:', expires=60 * 60 * 6):
            # cache key will look like 'musicbrainz:ab876bnb987'
            self.prefix = prefix
            # Cache values will expire after 6 hours
            self.expires = expires

        def build_key(self, url, args, method):
            # We want to prefix the cache key with a custom value
            return self.prefix + super().build_key(key, url, args, method)

        def get(self, key, url, args, method):
            """Called to get a value from the cache"""
            from_cache = redis_client.get(key)
            if not from_cache:
                # It's important to raise the exception here
                # So musicbrainz can send the actual HTTP request
                # if no value is found
                raise musicbrainzngs.cache.NotInCache(key)
            return from_cache

        def set(self, key, value, url, args, method):
            """Called to store a value in the cache"""
            redis_client.setex(key, value, self.expires)

    redis_cache = RedisCache()

    musicbrainzngs.set_cache(redis_cache)

Disabling the cache
-------------------

If, for some reason, you want to disable the cache, just run:

.. code-block:: python

    musicbrainzngs.set_cache(None)
