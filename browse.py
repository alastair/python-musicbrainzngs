
from pprint import pprint
import musicbrainz as m

RELEASE = '10269c7f-e208-478e-b688-4ca6472cfcf2'
LABEL = '47e718e1-7ee4-460c-b1cc-1192a841c6e5'

def main():
    pprint(m.browse_release(label=LABEL, limit=3, release_status='official'))
    pprint(m.browse_artist(release=RELEASE, limit=3))
    pprint(m.browse_label(release=RELEASE, limit=3))
    pprint(m.browse_recording(release=RELEASE, limit=3))
    pprint(m.browse_release_group(release=RELEASE, limit=3,
                                  release_type='album'))
    try:
        pprint(m.browse_artist(release=RELEASE, recording='asdhfjkad'))
    except Exception, e:
        print 'Okay:', e
        pass
    else:
        print '>>> Error: browse_artist accepted mutal exclusive selectors.'

if __name__ == "__main__":
    main()
