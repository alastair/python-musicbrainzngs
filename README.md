## Musicbrainz NGS bindings

This library implements webservice bindings for the Musicbrainz NGS site, also known as /ws/2.

For more information on the musicbrainz webservice see <http://wiki.musicbrainz.org/XML_Web_Service>.

### Usage

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

See the query.py file for more examples.

More documentation is available at https://python-musicbrainz-ngs.readthedocs.org

### Contribute

1. Fork the [repository](https://github.com/alastair/python-musicbrainz-ngs) on Github.
2. Make and test whatever changes you desire.
3. Signoff and commit your changes using `git commit -s`.
4. Send a pull request.

### Authors

These bindings were written by [Alastair Porter](http://github.com/alastair).
Contributions have been made by:

* [Adrian Sampson](https://github.com/sampsyo)
* [Galen Hazelwood](https://github.com/galenhz)
* [Greg Ward](https://github.com/gward)
* [Ian McEwen](https://github.com/ianmcorvidae)
* [Johannes Dewender](https://github.com/JonnyJD)
* [Michael Marineau](https://github.com/marineam)
* [Patrick Speiser](https://github.com/doskir)
* [Paul Bailey](https://github.com/paulbailey)
* [Sam Doshi](https://github.com/samdoshi)
* [Thomas Vander Stichele](https://github.com/thomasvs)
* [Wieland Hoffmann](https://github.com/mineo)

### License

This library is released under the simplified BSD license. See COPYING for details.
