#!/usr/bin/env python
"""A simple script that searches for a release in the MusicBrainz
database and prints out a few details about the first 5 matching release.

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
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

def show_release_details(rel):
    """Print some details about a release dictionary to stdout.
    """
    # "artist-credit-phrase" is a flat string of the credited artists
    # joined with " + " or whatever is given by the server.
    # You can also work with the "artist-credit" list manually.
    print("{}, by {}".format(rel['title'], rel["artist-credit-phrase"]))
    if 'date' in rel:
        print("Released {} ({})".format(rel['date'], rel['status']))
    print("MusicBrainz ID: {}".format(rel['id']))

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 2:
        sys.exit("usage: {} ARTIST ALBUM".format(sys.argv[0]))
    artist, album = args

    # Keyword arguments to the "search_*" functions limit keywords to
    # specific fields. The "limit" keyword argument is special (like as
    # "offset", not shown here) and specifies the number of results to
    # return.
    result = musicbrainzngs.search_releases(artist=artist, release=album,
                                            limit=5)
    # On success, result is a dictionary with a single key:
    # "release-list", which is a list of dictionaries.
    if not result['release-list']:
        sys.exit("no release found")
    for (idx, release) in enumerate(result['release-list']):
        print("match #{}:".format(idx+1))
        show_release_details(release)
        print()
