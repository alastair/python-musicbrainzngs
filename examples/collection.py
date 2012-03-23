#!/usr/bin/env python
"""View and modify your MusicBrainz collections.

To show a list of your collections:

    $ ./collection.py USERNAME
    Password for USERNAME: 
    All collections for this user:
    My Collection by USERNAME (4137a646-a104-4031-b549-da4e1f36a463) 

To show the releases in a collection:

    $ ./collection.py USERNAME 4137a646-a104-4031-b549-da4e1f36a463
    Password for USERNAME: 
    Releases in My Collection:
    None Shall Pass (b0885908-cbe2-4e51-95d8-c4f3b9721ad6)
    ...
"""
from __future__ import print_function
import musicbrainzngs
import getpass
from optparse import OptionParser

musicbrainzngs.set_useragent(
    "python-musicbrainz-ngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainz-ngs/",
)

def show_collections():
    """Fetch and display the current user's collections.
    """
    result = musicbrainzngs.get_collections()
    print('All collections for this user:')
    for collection in result['collection-list']:
        print('{name} by {editor} ({id})'.format(**collection))

def show_collection(collection_id):
    """Show the list of releases in a given collection.
    """
    result = musicbrainzngs.get_releases_in_collection(collection_id)
    collection = result['collection']
    print('Releases in {}:'.format(collection['name']))
    for release in collection['release-list']:
        print('{title} ({id})'.format(**release))

if __name__ == '__main__':
    parser = OptionParser(usage="%prog [options] USERNAME [COLLECTION-ID]")
    options, args = parser.parse_args()

    if not args:
        parser.error('no username specified')
    username = args.pop(0)

    # Input the password.
    password = getpass.getpass('Password for {}: '.format(username))

    # Call musicbrainzngs.auth() before making any API calls that
    # require authentication.
    musicbrainzngs.auth(username, password)

    if args:
        # Show a specific collection.
        show_collection(args[0])
    else:
        # Show all collections.
        show_collections()
