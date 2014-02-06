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

To add a release to a collection or remove one:

    $ ./collection.py USERNAME 4137a646-a104-4031-b549-da4e1f36a463
        --add 0d432d8b-8865-4ae9-8479-3a197620a37b
    $ ./collection.py USERNAME 4137a646-a104-4031-b549-da4e1f36a463
        --remove 0d432d8b-8865-4ae9-8479-3a197620a37b
"""
from __future__ import print_function
from __future__ import unicode_literals
import musicbrainzngs
import getpass
from optparse import OptionParser

try:
    user_input = raw_input
except NameError:
    user_input = input

musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

def show_collections():
    """Fetch and display the current user's collections.
    """
    result = musicbrainzngs.get_collections()
    print('All collections for this user:')
    for collection in result['collection-list']:
        print('{name} by {editor} ({mbid})'.format(
            name=collection['name'], editor=collection['editor'],
            mbid=collection['id']
        ))

def show_collection(collection_id):
    """Show the list of releases in a given collection.
    """
    result = musicbrainzngs.get_releases_in_collection(collection_id, limit=25)
    collection = result['collection']
    release_list = collection['release-list']
    # release count is only available starting with musicbrainzngs 0.5
    if "release-count" in collection:
        release_count = collection['release-count']
        print('{} releases in {}:'.format(release_count, collection['name']))
    else:
        print('Releases in {}:'.format(collection['name']))
    releases_fetched = 0
    while len(release_list) > 0:
        print("")
        releases_fetched += len(release_list)
        for release in release_list:
            print('{title} ({mbid})'.format(
                title=release['title'], mbid=release['id']
            ))
        if user_input("Would you like to display more releases? [y/N] ") != "y":
            break;

        # fetch next batch of releases
        result = musicbrainzngs.get_releases_in_collection(collection_id,
                            limit=25, offset=releases_fetched)
        collection = result['collection']
        release_list = collection['release-list']

    print("")
    print("Number of fetched releases: %d" % releases_fetched)

if __name__ == '__main__':
    parser = OptionParser(usage="%prog [options] USERNAME [COLLECTION-ID]")
    parser.add_option('-a', '--add', metavar="RELEASE-ID",
                      help="add a release to the collection")
    parser.add_option('-r', '--remove', metavar="RELEASE-ID",
                      help="remove a release from the collection")
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
        # Actions for a specific collction.
        collection_id = args[0]
        if options.add:
            # Add a release to the collection.
            musicbrainzngs.add_releases_to_collection(
                collection_id, [options.add]
            )
        elif options.remove:
            # Remove a release from the collection.
            musicbrainzngs.remove_releases_from_collection(
                collection_id, [options.remove]
            )
        else:
            # Print out the collection's contents.
            print("")
            show_collection(collection_id)
    else:
        # Show all collections.
        print("")
        show_collections()
