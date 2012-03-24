#!/usr/bin/env python
"""A simple script that searches for a release in the MusicBrainz
database and prints out a few details about the first matching release.

    $ ./releasesearch.py "the beatles" revolver
    Revolver, by The Beatles
    Released 1966-08-08 (Official)
    MusicBrainz ID: b4b04cbf-118a-3944-9545-38a0a88ff1a2
"""
from __future__ import print_function
from __future__ import unicode_literals
import musicbrainzngs
import sys

musicbrainzngs.set_useragent(
    "python-musicbrainz-ngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainz-ngs/",
)

def show_release_details(rel):
    """Print some details about a release dictionary to stdout.
    """
    artist_names = [c['artist']['name'] for c in rel['artist-credit']]
    print("{}, by {}".format(rel['title'], ', '.join(artist_names)))
    if 'date' in rel:
        print("Released {} ({})".format(rel['date'], rel['status']))
    print("MusicBrainz ID: {}".format(rel['id']))

def fail(message):
    """Print a message to stderr and then exit with an error status.
    """
    print(message, file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 2:
        fail("usage: {} ARTIST ALBUM".format(sys.argv[0]))
    artist, album = args

    # Keyword arguments to the "search_*" functions limit keywords to
    # specific fields. The "limit" keyword argument is special (like as
    # "offset", not shown here) and specifies the number of results to
    # return.
    result = musicbrainzngs.search_releases(artist=artist, release=album,
                                            limit=1)
    # On success, result is a dictionary with a single key:
    # "release-list", which is a list of dictionaries.
    if not result['release-list']:
        fail("no release found")
    show_release_details(result['release-list'][0])
