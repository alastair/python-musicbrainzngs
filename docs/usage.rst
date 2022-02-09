Usage
~~~~~

In general you need to set a useragent for your application,
start searches to get to know corresponding MusicBrainz IDs
and then retrieve information about these entities.

The data is returned in form of a :class:`dict`.

If you also want to submit data,
then you must authenticate as a MusicBrainz user.

This part of the documentation will give you usage examples.
For an overview of available functions you can have a look at
the :doc:`api`.

Identification
--------------

To access the MusicBrainz webservice through this library, you `need to
identify your application
<http://musicbrainz.org/doc/XML_Web_Service/Version_2#Identifying_your_application_to_the_MusicBrainz_Web_Service>`_
by setting the useragent header made in HTTP requests to one that is unique to
your application.

To ease this, the convenience function :meth:`musicbrainzngs.set_useragent` is
provided which automatically sets the useragent based on information about the
application name, version and contact information to the format `recommended by
MusicBrainz
<http://musicbrainz.org/doc/XML_Web_Service/Rate_Limiting#Provide_meaningful_User-Agent_strings>`_.

If a request is made without setting the useragent beforehand, a
:exc:`musicbrainzngs.UsageError` will be raised.

Authentication
--------------

Certain calls to the webservice require user authentication prior to the call
itself. The affected functions state this requirement in their documentation.
The user and password used for authentication are the same as for the
MusicBrainz website itself and can be set with the :meth:`musicbrainzngs.auth`
method. After calling this function, the credentials will be saved and
automatically used by all functions requiring them.

If a method requiring authentication is called without authenticating, a
:exc:`musicbrainzngs.UsageError` will be raised.

If the credentials provided are wrong and the server returns a status code of
401, a :exc:`musicbrainzngs.AuthenticationError` will be raised.

Getting Data
------------

Regular MusicBrainz Data
^^^^^^^^^^^^^^^^^^^^^^^^

You can get MusicBrainz entities as a :class:`dict`
when retrieving them with some form of identifier.
An example using :func:`musicbrainzngs.get_artist_by_id`::

  artist_id = "c5c2ea1c-4bde-4f4d-bd0b-47b200bf99d6"
  try:
      result = musicbrainzngs.get_artist_by_id(artist_id)
  except WebServiceError as exc:
      print("Something went wrong with the request: %s" % exc)
  else:
      artist = result["artist"]
      print("name:\t\t%s" % artist["name"])
      print("sort name:\t%s" % artist["sort-name"])

You can get more information about entities connected to the artist
with adding `includes` and you filter releases and release_groups::

  result = musicbrainzngs.get_artist_by_id(artist_id,
                includes=["release-groups"], release_type=["album", "ep"])
  for release_group in result["artist"]["release-group-list"]:
      print("{title} ({type})".format(title=release_group["title"],
                                      type=release_group["type"]))

.. tip:: Compilations are also of primary type "album".
   You have to filter these out manually if you don't want them.

.. note:: You can only get at most 25 release groups using this method.
   If you want to fetch all release groups you will have to
   `browse <browsing>`_.

Cover Art Data
^^^^^^^^^^^^^^

This library includes a few methods to access data from the `Cover Art Archive
<https://coverartarchive.org/>`_ which has a `documented API
<https://musicbrainz.org/doc/Cover_Art_Archive/API>`_.

Both :func:`musicbrainzngs.get_image_list` and
:func:`musicbrainzngs.get_release_group_image_list` return the deserialized
cover art listing for a `release
<https://musicbrainz.org/doc/Cover_Art_Archive/API#.2Frelease.2F.7Bmbid.7D.2F>`_
or `release group
<https://musicbrainz.org/doc/Cover_Art_Archive/API#.2Frelease-group.2F.7Bmbid.7D.2F>`_.
To find out whether a release
has an approved front image, you could use the following example code::

  release_id = "46a48e90-819b-4bed-81fa-5ca8aa33fbf3"
  data = musicbrainzngs.get_cover_art_list("46a48e90-819b-4bed-81fa-5ca8aa33fbf3")
  for image in data["images"]:
      if "Front" in image["types"] and image["approved"]:
          print "%s is an approved front image!" % image["thumbnails"]["large"]
          break

To retrieve an image itself, use :func:`musicbrainzngs.get_image`. A
few convenience functions like :func:`musicbrainzngs.get_image_front`
are provided to allow easy access to often requested images.

.. warning:: There is no upper bound for the size of images uploaded to the
   Cover Art Archive and downloading an image will return the binary data in
   memory. Consider using the :py:mod:`tempfile` module or similar
   techniques to save images to disk as soon as possible.

Searching
---------

When you don't know the MusicBrainz IDs yet, you have to start a search.
Using :func:`musicbrainzngs.search_artists`::

  result = musicbrainzngs.search_artists(artist="xx", type="group",
                                         country="GB")
  for artist in result['artist-list']:
      print(u"{id}: {name}".format(id=artist['id'], name=artist["name"]))

.. tip:: Musicbrainzngs returns unicode strings.
   It's up to you to make sure Python (2) doesn't try to convert these
   to ascii again. In the example we force a unicode literal for print.
   Python 3 works without fixes like these.

You can also use the query without specifying the search fields::

  musicbrainzngs.search_release_groups("the clash london calling")

The query and the search fields can also be used at the same time.

Browsing
--------

When you want to fetch a list of entities greater than 25,
you have to use one of the browse functions.
Not only can you specify a `limit` as high as 100,
but you can also specify an `offset` to get the complete list
in multiple requests.

An example would be using :func:`musicbrainzngs.browse_release_groups`
to get all releases for a label::

  label = "71247f6b-fd24-4a56-89a2-23512f006f0c"
  limit = 100
  offset = 0
  releases = []
  page = 1
  print("fetching page number %d.." % page)
  result = musicbrainzngs.browse_releases(label=label, includes=["labels"],
                  release_type=["album"], limit=limit)
  page_releases = result['release-list']
  releases += page_releases
  # release-count is only available starting with musicbrainzngs 0.5
  if "release-count" in result:
          count = result['release-count']
          print("")
  while len(page_releases) >= limit:
      offset += limit
      page += 1
      print("fetching page number %d.." % page)
      result = musicbrainzngs.browse_releases(label=label, includes=["labels"],
                          release_type=["album"], limit=limit, offset=offset)
      page_releases = result['release-list']
      releases += page_releases
  print("")
  for release in releases:
      for label_info in release['label-info-list']:
          catnum = label_info.get('catalog-number')
          if label_info['label']['id'] == label and catnum:
              print("{catnum:>17}: {date:10} {title}".format(catnum=catnum,
                          date=release['date'], title=release['title']))
  print("\n%d releases on  %d pages" % (len(releases), page))

.. tip:: You should always try to filter in the query, when possible,
   rather than fetching everything and filtering afterwards.
   This will make your application faster
   since web service requests are throttled.
   In the example we filter by `release_type`.

Submitting
----------

You can also submit data using musicbrainzngs.
Please use :func:`musicbrainzngs.set_hostname` to set the host to
test.musicbrainz.org when testing the submission part of your application.

`Authentication`_ is necessary to submit any data to MusicBrainz.

An example using :func:`musicbrainzngs.submit_barcodes` looks like this::

  musicbrainzngs.set_hostname("test.musicbrainz.org")
  musicbrainzngs.auth("test", "mb")

  barcodes = {
      "174a5513-73d1-3c9d-a316-3c1c179e35f8": "5099749534728",
      "838952af-600d-3f51-84d5-941d15880400": "602517737280"
  }
  musicbrainzngs.submit_barcodes(barcodes)

See :ref:`api_submitting` in the API for other possibilities.

More Examples
-------------

You can find some examples for using `musicbrainzngs` in the
`examples directory <https://github.com/alastair/python-musicbrainzngs/tree/master/examples>`_.
