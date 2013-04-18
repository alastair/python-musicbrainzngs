Usage
~~~~~

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
automaticall used by all functions requiring them.

If a method requiring authentication is called without authenticating, a
:exc:`musicbrainzngs.UsageError` will be raised.

If the credentials provided are wrong and the server returns a status code of
401, a :exc:`musicbrainzngs.AuthenticationError` will be raised.

Getting data
------------

You can get MusicBrainz entities as a :class:`dict`
when retrieving them with some form of identifier.
An example using :func:`musicbrainzngs.get_artist_by_id`::

  artist_id = "c5c2ea1c-4bde-4f4d-bd0b-47b200bf99d6"
  try:
      musicbrainzngs.get_artist_by_id(artist_id)
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

Searching
---------

When you don't know the MusicBrainz IDs yet, you have to start a search.
Using :func:`musicbrainzngs.search_artist`::

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

Submitting
----------
