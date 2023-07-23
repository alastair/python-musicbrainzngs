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
    print(f"\t{rel['title']}")
    print(f"\t\tMusicBrainz ID: {rel['id']}")
    if rel.get('barcode'):
        print(f"\t\tEAN/UPC: {rel['barcode']}")
    for info in rel['label-info-list']:
        if info.get('catalog-number'):
            print(f"\t\tcat#: {info['catalog-number']}")

def show_offsets(offset_list):
    offsets = None
    for offset in offset_list:
        if offsets is None:
            offsets = str(offset)
        else:
            offsets += f" {str(offset)}"
    print(f"\toffsets: {offsets}")

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit(f"usage: {sys.argv[0]} DISC_ID")
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
        print(f"\tSectors: {result['disc']['sectors']}")
        # offset-list only available starting with musicbrainzngs 0.6
        if "offset-list" in result['disc']:
            show_offsets(result['disc']['offset-list'])
            print(f"\tTracks: {result['disc']['offset-count']}")
        for release in result['disc']['release-list']:
            show_release_details(release)
            print("")
    elif result.get('cdstub'):
        print("cdstub:")
        print(f"\tArtist: {result['cdstub']['artist']}")
        print(f"\tTitle: {result['cdstub']['title']}")
        if result['cdstub'].get('barcode'):
            print(f"\tBarcode: {result['cdstub']['barcode']}")
    else:
        sys.exit("no valid results")
