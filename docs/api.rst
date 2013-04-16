API
~~~

General
-------

.. autofunction:: musicbrainzngs.auth

.. autofunction:: musicbrainzngs.set_rate_limit

.. autofunction:: musicbrainzngs.set_useragent

.. autofunction:: musicbrainzngs.set_hostname

Getting data
------------

.. autofunction:: musicbrainzngs.get_artist_by_id

.. autofunction:: musicbrainzngs.get_label_by_id

.. autofunction:: musicbrainzngs.get_recording_by_id

.. autofunction:: musicbrainzngs.get_recordings_by_echoprint

.. autofunction:: musicbrainzngs.get_recordings_by_puid

.. autofunction:: musicbrainzngs.get_recordings_by_isrc

.. autofunction:: musicbrainzngs.get_release_group_by_id

.. autofunction:: musicbrainzngs.get_release_by_id

.. autofunction:: musicbrainzngs.get_releases_by_discid

.. autofunction:: musicbrainzngs.get_work_by_id

.. autofunction:: musicbrainzngs.get_works_by_iswc

.. autofunction:: musicbrainzngs.get_collections

.. autofunction:: musicbrainzngs.get_releases_in_collection

.. _search_api:

Searching
---------

For all of these search functions you can use any of the allowed search fields
as parameter names.
You can also set the `query` parameter to any lucene query you like.
When you use any of the search fields as parameters,
special characters are escaped in the `query`.

By default the elements are concatenated with spaces in between,
so lucene essentially does a fuzzy search.
That search might include results that don't match the complete query,
though these will be ranked lower than the ones that do.
If you want all query elements to match for all results,
you have to set `strict=True`.

.. autofunction:: musicbrainzngs.search_annotations

.. autofunction:: musicbrainzngs.search_artists

.. autofunction:: musicbrainzngs.search_labels

.. autofunction:: musicbrainzngs.search_recordings

.. autofunction:: musicbrainzngs.search_release_groups

.. autofunction:: musicbrainzngs.search_releases

.. autoattribute:: musicbrainzngs.musicbrainz.VALID_INCLUDES

.. autoattribute:: musicbrainzngs.musicbrainz.VALID_SEARCH_FIELDS

Browsing
--------

.. autofunction:: musicbrainzngs.browse_artists

.. autofunction:: musicbrainzngs.browse_labels

.. autofunction:: musicbrainzngs.browse_recordings

.. autofunction:: musicbrainzngs.browse_release_groups

.. autofunction:: musicbrainzngs.browse_releases

Submitting
----------

.. autofunction:: musicbrainzngs.submit_barcodes

.. autofunction:: musicbrainzngs.submit_puids

.. autofunction:: musicbrainzngs.submit_echoprints

.. autofunction:: musicbrainzngs.submit_isrcs

.. autofunction:: musicbrainzngs.submit_tags

.. autofunction:: musicbrainzngs.submit_ratings

.. autofunction:: musicbrainzngs.add_releases_to_collection

.. autofunction:: musicbrainzngs.remove_releases_from_collection

Exceptions
----------

.. autoclass:: musicbrainzngs.MusicBrainzError

.. autoclass:: musicbrainzngs.UsageError
   :show-inheritance:

.. autoclass:: musicbrainzngs.WebServiceError
   :show-inheritance:

.. autoclass:: musicbrainzngs.AuthenticationError
   :show-inheritance:

.. autoclass:: musicbrainzngs.NetworkError
   :show-inheritance:

.. autoclass:: musicbrainzngs.ResponseError
   :show-inheritance:
