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

General
-------

.. autofunction:: auth
.. autofunction:: set_rate_limit
.. autofunction:: set_useragent
.. autofunction:: set_hostname

Getting data
------------

All of these functions will fetch a MusicBrainz entity or a list of entities
as a dict.
You can specify a list of `includes` to get more data
and you can filter on `release_status` and `release_type`.
See :const:`musicbrainz.VALID_RELEASE_STATUSES`
and :const:`musicbrainz.VALID_RELEASE_TYPES`.
The valid includes are listed for each function.

.. autofunction:: get_artist_by_id
.. autofunction:: get_label_by_id
.. autofunction:: get_recording_by_id
.. autofunction:: get_recordings_by_echoprint
.. autofunction:: get_recordings_by_puid
.. autofunction:: get_recordings_by_isrc
.. autofunction:: get_release_group_by_id
.. autofunction:: get_release_by_id
.. autofunction:: get_releases_by_discid
.. autofunction:: get_work_by_id
.. autofunction:: get_works_by_iswc
.. autofunction:: get_collections
.. autofunction:: get_releases_in_collection

.. autoattribute:: musicbrainz.VALID_RELEASE_TYPES
.. autoattribute:: musicbrainz.VALID_RELEASE_STATUSES

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

.. autofunction:: search_annotations
.. autofunction:: search_artists
.. autofunction:: search_labels
.. autofunction:: search_recordings
.. autofunction:: search_release_groups
.. autofunction:: search_releases

.. autoattribute:: musicbrainz.VALID_INCLUDES

Browsing
--------

.. autofunction:: browse_artists
.. autofunction:: browse_labels
.. autofunction:: browse_recordings
.. autofunction:: browse_release_groups
.. autofunction:: browse_releases

Submitting
----------

.. autofunction:: submit_barcodes
.. autofunction:: submit_puids
.. autofunction:: submit_echoprints
.. autofunction:: submit_isrcs
.. autofunction:: submit_tags
.. autofunction:: submit_ratings
.. autofunction:: add_releases_to_collection
.. autofunction:: remove_releases_from_collection

Exceptions
----------

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
