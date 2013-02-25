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

.. autoclass:: musicbrainzngs.AuthenticationError

.. autoclass:: musicbrainzngs.UsageError
