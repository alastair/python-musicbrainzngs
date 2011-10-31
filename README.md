## Musicbrainz NGS bindings

This library implements webservice bindings for the Musicbrainz NGS
site, commonly known as /ws/2

For more information, see http://wiki.musicbrainz.org/XML_Web_Service

Requires Python 2.4 or newer.

### Usage

    # Import the module
    import musicbrainz

    # If you plan to submit data, authenticate
    musicbrainz.auth("user", "password")

    # If you are connecting to a development server
    musicbrainz.hostname = "echoprint.musicbrainz.org"

See the query.py file for more examples

### Authors

These bindings were written by [Alastair
Porter](http://github.com/alastair). Contributions have been made by
[Adrian Sampson](https://github.com/sampsyo) and [Hartmut Goebel][https://github.com/htgoebel].

### License

This library is released under the simplified BSD license. See COPYING
for details.
