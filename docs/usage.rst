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
:class:`musicbrainzngs.UsageError` will be raised.

Authentication
--------------

Certain calls to the webservice require user authentication prior to the call
itself. The affected functions state this requirement in their documentation.
The user and password used for authentication are the same as for the
MusicBrainz website itself and can be set with the :meth:`musicbrainzngs.auth`
method. After calling this function, the credentials will be saved and
automaticall used by all functions requiring them.

If a method requiring authentication is called without authenticating, a
:class:`musicbrainzngs.UsageError` will be raised.

If the credentials provided are wrong and the server returns a status code of
401, a :class:`musicbrainzngs.AuthenticationError` will be raised.

Getting data
------------

Searching
---------

Browsing
--------

Submitting
----------
