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
    returns a dummy response or raises an exception """
    def __init__(self, response="<response/>", exception=None):
        self.myurl = None
        self.response = response
        self.exception = exception

    def open(self, request, body=None):
        self.myurl = request.get_full_url()
        self.request = request
        if self.exception:
            raise self.exception
        else:
            return StringIO.StringIO(self.response)

    def get_url(self):
        return self.myurl


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
