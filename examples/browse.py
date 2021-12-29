#!/usr/bin/env python
"""
Browse entities on musicbrainz
"""
import json
import sys
from argparse import ArgumentParser

import musicbrainzngs

musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        "entity_type",
        choices=["collection"],
        help="The type of entity we're trying to get"
    )
    parser.add_argument("linked_entity_type", help="The entity type it's linked to")
    parser.add_argument("mbid", help="The ID of the linked entity")
    args = parser.parse_args()

    result = {}
    if args.entity_type == "collection":
        result = musicbrainzngs.browse_collections(args.linked_entity_type, args.mbid)
    else:
        print("Invalid entity type passed", file=sys.stderr)
        exit(1)
    print(json.dumps(result, indent=2))
