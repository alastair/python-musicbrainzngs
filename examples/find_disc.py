#!/usr/bin/env python
"""A script that looks for a release in the MusicBrainz database by disc ID

    $ ./find_disc.py kKOqMEuRDSeW_.K49SUEJXensLY-
    disc:
        Sectors: 295099
        London Calling
            MusicBrainz ID: 174a5513-73d1-3c9d-a316-3c1c179e35f8
            EAN/UPC: 5099749534728
            cat#: 495347 2

        ...
"""

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
    print("\t{}".format(rel['title']))
    print("\t\tMusicBrainz ID: {}".format(rel['id']))
    if rel.get('barcode'):
        print("\t\tEAN/UPC: {}".format(rel['barcode']))
    for info in rel['label-info-list']:
        if info.get('catalog-number'):
            print("\t\tcat#: {}".format(info['catalog-number']))

def show_offsets(offset_list):
    offsets = None
    for offset in offset_list:
        if offsets == None:
            offsets = str(offset)
        else:
            offsets += " " + str(offset)
    print("\toffsets: {}".format(offsets))

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit("usage: {} DISC_ID".format(sys.argv[0]))
    discid = args[0]

    try:
        # the "labels" include enables the cat#s we display
        result = musicbrainzngs.get_releases_by_discid(discid,
                includes=["labels"])
    except musicbrainzngs.ResponseError as err:
        if err.cause.code == 404:
            sys.exit("disc not found")
        else:
            sys.exit("received bad response from the MB server")

    # The result can either be a "disc" or a "cdstub"
    if result.get('disc'):
        print("disc:")
        print("\tSectors: {}".format(result['disc']['sectors']))
        # offset-list only available starting with musicbrainzngs 0.6
        if "offset-list" in result['disc']:
            show_offsets(result['disc']['offset-list'])
            print("\tTracks: {}".format(result['disc']['offset-count']))
        for release in result['disc']['release-list']:
            show_release_details(release)
            print("")
    elif result.get('cdstub'):
        print("cdstub:")
        print("\tArtist: {}".format(result['cdstub']['artist']))
        print("\tTitle: {}".format(result['cdstub']['title']))
        if result['cdstub'].get('barcode'):
            print("\tBarcode: {}".format(result['cdstub']['barcode']))
    else:
        sys.exit("no valid results")
