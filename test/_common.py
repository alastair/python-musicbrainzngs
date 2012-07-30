"""Common support for the test cases."""
import time

import musicbrainzngs
from musicbrainzngs import compat

try:
    from urllib2 import OpenerDirector
except ImportError:
    from urllib.request import OpenerDirector
try:
    import StringIO
except ImportError:
    import io as StringIO

class FakeOpener(OpenerDirector):
    """ A URL Opener that saves the URL requested and
    returns a dummy response """
    def __init__(self):
        self.myurl = None

    def open(self, request, body=None):
        self.myurl = request.get_full_url()
        self.request = request
        return StringIO.StringIO("<response/>")

    def get_url(self):
        return self.myurl

opener = FakeOpener()
musicbrainzngs.compat.build_opener = lambda *args: opener

# Mock timing.
class Timecop(object):
    """Mocks the timing system (namely time() and sleep()) for testing.
    Inspired by the Ruby timecop library.
    """
    def __init__(self):
        self.now = time.time()

    def time(self):
        return self.now

    def sleep(self, amount):
        self.now += amount

    def install(self):
        self.orig = {
            'time': time.time,
            'sleep': time.sleep,
        }
        time.time = self.time
        time.sleep = self.sleep

    def restore(self):
        time.time = self.orig['time']
        time.sleep = self.orig['sleep']
