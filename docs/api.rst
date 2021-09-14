API
~~~
.. module:: musicbrainzngs

This is a shallow python binding of the MusicBrainz web service
so you should read
:musicbrainz:`Development/XML Web Service/Version 2`
to understand how that web service works in general.

All requests that fetch data return the data in the form of a :class:`dict`.
Attributes and elements both map to keys in the dict.
List entities are of type :class:`list`.

This part will give an overview of available functions.
Have a look at :doc:`usage` for examples on how to use them.

General
-------

.. autofunction:: auth
.. autofunction:: set_rate_limit
.. autofunction:: set_useragent
.. autofunction:: set_hostname
.. autofunction:: set_caa_hostname
.. autofunction:: set_parser
.. autofunction:: set_format

Getting Data
------------

All of these functions will fetch a MusicBrainz entity or a list of entities
as a dict.
You can specify a list of `includes` to get more data
and you can filter on `release_status` and `release_type`.
See :const:`musicbrainz.VALID_RELEASE_STATUSES`
and :const:`musicbrainz.VALID_RELEASE_TYPES`.
The valid includes are listed for each function.

.. autofunction:: get_area_by_id
.. autofunction:: get_artist_by_id
.. autofunction:: get_event_by_id
.. autofunction:: get_instrument_by_id
.. autofunction:: get_label_by_id
.. autofunction:: get_place_by_id
.. autofunction:: get_recording_by_id
.. autofunction:: get_recordings_by_isrc
.. autofunction:: get_release_group_by_id
.. autofunction:: get_release_by_id
.. autofunction:: get_releases_by_discid
.. autofunction:: get_series_by_id
.. autofunction:: get_work_by_id
.. autofunction:: get_works_by_iswc
.. autofunction:: get_url_by_id
.. autofunction:: get_collections
.. autofunction:: get_releases_in_collection

.. autodata:: musicbrainzngs.musicbrainz.VALID_RELEASE_TYPES
.. autodata:: musicbrainzngs.musicbrainz.VALID_RELEASE_STATUSES

.. _caa_api:

Cover Art
---------

.. autofunction:: get_image_list
.. autofunction:: get_release_group_image_list
.. autofunction:: get_image
.. autofunction:: get_image_front
.. autofunction:: get_release_group_image_front
.. autofunction:: get_image_back


.. _search_api:

Searching
---------

For all of these search functions you can use any of the allowed search fields
as parameter names.
The documentation of what these fields do is on
:musicbrainz:`Development/XML Web Service/Version 2/Search`.

You can also set the `query` parameter to any lucene query you like.
When you use any of the search fields as parameters,
special characters are escaped in the `query`.

By default the elements are concatenated with spaces in between,
so lucene essentially does a fuzzy search.
That search might include results that don't match the complete query,
though these will be ranked lower than the ones that do.
If you want all query elements to match for all results,
you have to set `strict=True`.

By default the web service returns 25 results per request and you can set
a `limit` of up to 100.
You have to use the `offset` parameter to set how many results you have
already seen so the web service doesn't give you the same results again.

.. autofunction:: search_annotations
.. autofunction:: search_areas
.. autofunction:: search_artists
.. autofunction:: search_events
.. autofunction:: search_instruments
.. autofunction:: search_labels
.. autofunction:: search_places
.. autofunction:: search_recordings
.. autofunction:: search_release_groups
.. autofunction:: search_releases
.. autofunction:: search_series
.. autofunction:: search_works

Browsing
--------

You can browse entities of a certain type linked to one specific entity.
That is you can browse all recordings by an artist, for example.

These functions can be used to to include more than the maximum of 25 linked
entities returned by the functions in `Getting Data`_.
You can set a `limit` as high as 100. The default is still 25.
Similar to the functions in `Searching`_, you have to specify
an `offset` to see the results you haven't seen yet.

You have to provide exactly one MusicBrainz ID to these functions.

.. autofunction:: browse_artists
.. autofunction:: browse_events
.. autofunction:: browse_labels
.. autofunction:: browse_places
.. autofunction:: browse_recordings
.. autofunction:: browse_release_groups
.. autofunction:: browse_releases
.. autofunction:: browse_urls

.. _api_submitting:

Submitting
----------

These are the only functions that write to the MusicBrainz database.
They take one or more dicts with multiple entities as keys,
which take certain values or a list of values.

You have to use :func:`auth` before using any of these functions.

.. autofunction:: submit_barcodes
.. autofunction:: submit_isrcs
.. autofunction:: submit_tags
.. autofunction:: submit_ratings
.. autofunction:: add_releases_to_collection
.. autofunction:: remove_releases_from_collection

Exceptions
----------

These are the main exceptions that are raised by functions in musicbrainzngs.
You might want to catch some of these at an appropriate point in your code.

Some of these might have subclasses that are not listed here.

.. autoclass:: MusicBrainzError

.. autoclass:: UsageError
   :show-inheritance:

.. autoclass:: WebServiceError
   :show-inheritance:

.. autoclass:: AuthenticationError
   :show-inheritance:

.. autoclass:: NetworkError
   :show-inheritance:

.. autoclass:: ResponseError
   :show-inheritance:

Logging
-------

`musicbrainzngs` logs debug and informational messages using Python's
:mod:`logging` module.
All logging is done in the logger with the name `musicbrainzngs`.

You can enable this output in your application with::

    import logging
    logging.basicConfig(level=logging.DEBUG)
    # optionally restrict musicbrainzngs output to INFO messages
    logging.getLogger("musicbrainzngs").setLevel(logging.INFO)
