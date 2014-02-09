Musicbrainz NGS bindings
########################

This library implements webservice bindings for the Musicbrainz NGS site, also known as /ws/2.

For more information on the musicbrainz webservice see `<http://wiki.musicbrainz.org/XML_Web_Service>`_.

Usage
*****

::

    # Import the module
    import musicbrainzngs

    # If you plan to submit data, authenticate
    musicbrainzngs.auth("user", "password")

    # Tell musicbrainz what your app is, and how to contact you
    # (this step is required, as per the webservice access rules
    # at http://wiki.musicbrainz.org/XML_Web_Service/Rate_Limiting )
    musicbrainzngs.set_useragent("Example music app", "0.1", "http://example.com/music")

    # If you are connecting to a development server
    musicbrainzngs.set_hostname("echoprint.musicbrainz.org")

See the ``query.py`` file for more examples.

More documentation is available at
`Read the Docs <https://python-musicbrainzngs.readthedocs.org>`_.

Contribute
**********

1. Fork the `repository <https://github.com/alastair/python-musicbrainzngs>`_
   on Github.
2. Make and test whatever changes you desire.
3. Signoff and commit your changes using ``git commit -s``.
4. Send a pull request.

Authors
*******

These bindings were written by `Alastair Porter <http://github.com/alastair>`_.
Contributions have been made by:

* `Adrian Sampson <https://github.com/sampsyo>`_
* `Galen Hazelwood <https://github.com/galenhz>`_
* `Greg Ward <https://github.com/gward>`_
* `Ian McEwen <https://github.com/ianmcorvidae>`_
* `Johannes Dewender <https://github.com/JonnyJD>`_
* `Michael Marineau <https://github.com/marineam>`_
* `Patrick Speiser <https://github.com/doskir>`_
* `Paul Bailey <https://github.com/paulbailey>`_
* `Ryan Helinski <https://github.com/rlhelinski>`_
* `Sam Doshi <https://github.com/samdoshi>`_
* `Simon Chopin <https://github.com/laarmen>`_
* `Thomas Vander Stichele <https://github.com/thomasvs>`_
* `Wieland Hoffmann <https://github.com/mineo>`_

License
*******

This library is released under the simplified BSD license except for the file
``musicbrainzngs/compat.py`` which is licensed under the ISC license.
See COPYING for details.
