Musicbrainz NGS bindings
########################

This library implements webservice bindings for the Musicbrainz NGS site, also known as /ws/2
and the `Cover Art Archive <https://coverartarchive.org/>`_.

For more information on the musicbrainz webservice see `<http://wiki.musicbrainz.org/XML_Web_Service>`_.

Usage
*****

.. code:: python

    # Import the module
    import musicbrainzngs

    # If you plan to submit data, authenticate
    musicbrainzngs.auth("user", "password")

    # Tell musicbrainz what your app is, and how to contact you
    # (this step is required, as per the webservice access rules
    # at http://wiki.musicbrainz.org/XML_Web_Service/Rate_Limiting )
    musicbrainzngs.set_useragent("Example music app", "0.1", "http://example.com/music")

    # If you are connecting to a different server
    musicbrainzngs.set_hostname("beta.musicbrainz.org")

See the ``query.py`` file for more examples.

More documentation is available at
`Read the Docs <https://python-musicbrainzngs.readthedocs.org>`_.

Contribute
**********

If you want to contribute to this repository, please read `the
contribution guidelines
<https://github.com/alastair/python-musicbrainzngs/blob/master/CONTRIBUTING.md>`_ first.


Authors
*******

These bindings were written by `Alastair Porter <http://github.com/alastair>`_.
Contributions have been made by:

* `Adrian Sampson <https://github.com/sampsyo>`_
* `Corey Farwell <https://github.com/frewsxcv>`_
* `Galen Hazelwood <https://github.com/galenhz>`_
* `Greg Ward <https://github.com/gward>`_
* `Ian McEwen <https://github.com/ianmcorvidae>`_
* `Jérémie Detrey <https://github.com/jdetrey>`_
* `Johannes Dewender <https://github.com/JonnyJD>`_
* `Michael Marineau <https://github.com/marineam>`_
* `Patrick Speiser <https://github.com/doskir>`_
* `Pavan Chander <https://github.com/navap>`_
* `Paul Bailey <https://github.com/paulbailey>`_
* `Rui Gonçalves <https://github.com/ruippeixotog>`_
* `Ryan Helinski <https://github.com/rlhelinski>`_
* `Sam Doshi <https://github.com/samdoshi>`_
* `Shadab Zafar <https://github.com/dufferzafar>`_
* `Simon Chopin <https://github.com/laarmen>`_
* `Thomas Vander Stichele <https://github.com/thomasvs>`_
* `Wieland Hoffmann <https://github.com/mineo>`_

License
*******

This library is released under the simplified BSD license except for the file
``musicbrainzngs/compat.py`` which is licensed under the ISC license.
See COPYING for details.
