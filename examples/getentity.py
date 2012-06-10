#!/usr/bin/env python
"""Get entities based on ID.

To get details for an entity:

    $ ./getentity.py <entitytype> <id>

<entity> can be any of artist, label, recording, release, relasegroup, work
<id> is the musicbrainz id of any of these entities.

"""
from __future__ import print_function
from __future__ import unicode_literals
import sys
import musicbrainzngs
from optparse import OptionParser

musicbrainzngs.set_useragent(
    "python-musicbrainz-ngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainz-ngs/",
)

def get_artist(artistid):
    """ Get details about an artist """
    # Get simple metadata
    artist = musicbrainzngs.get_artist_by_id(artistid)

    # You can also get additional information, for example artist's releases.
    # Note that additional data is limited to 25 items. Use the browse functions
    # in order to get more.

    # Filter the releases that are included by their type (e.g. EP, Single, Album)
    # or their status (official, bootleg)

    # Get tags and ratings to see what people say about an artist

    # If you want to get tags that a single user has added to an entity then
    # that user must log in first.

def get_label(labelid):
    label = musicbrainzngs.get_label_by_id(labelid)

    # Get artists on a label. Note that this will only show a maximum of 25 artists.
    # use browse to see more.
    label = musicbrainzngs.get_label_by_id(labelid, includes=["artists"])

def get_recording(recordingid):
    pass

def get_release(releaseid):
    pass

def get_releasegroup(rgid):
    pass

def get_work(workid):
    # Get the recordings of a work, and the artists that performed each recording
    pass

if __name__ == '__main__':
    parser = OptionParser(usage="%prog ENTITY ENTITY-ID")
    options, args = parser.parse_args()

    if len(args) != 2:
        parser.print_usage()
        sys.exit(1)
    entity = args[0]
    eid = args[1]

    if entity == "work":
        get_work(eid)
    elif entity == "label":
        get_label(eid)
    elif entity == "recording":
        get_recording(eid)
    elif entity == "release":
        get_release(eid)
    elif entity == "releasegroup":
        get_releasegroup(eid)
    elif entity == "work":
        get_work(eid)
    else:
        print("Unknown entity {}".format(entity))
