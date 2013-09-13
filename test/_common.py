"""Common support for the test cases."""
from urllib.request import OpenerDirector

import requests_mock
import time
import musicbrainzngs


from os.path import join
from unittest import TestCase


class FakeOpener(OpenerDirector):
    """ A URL Opener that saves the URL requested and
    returns a dummy response or raises an exception """
    def __init__(self, response="<response/>", exception=None):
        self.myurl = None
        self.headers = None
        self.response = response
        self.exception = exception
        self.handlers = []


class RequestsMockingTestCase(TestCase):
    """Mocks requests HTTP layer by instantiating a requests_mock.Mocker in setUp
    and stopping it in tearDown. That object is available in the `m` attribute.

    """
    def setUp(self):
        self.m = requests_mock.Mocker()
        self.m.start()

    @property
    def last_url(self):
        """The last URL seen by the Mocker.
        """
        return self.m.request_history.pop().url

    def tearDown(self):
        self.m.stop()


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


def open_and_parse_test_data(datadir, filename):
    """ Opens an XML file dumped from the MusicBrainz web service and returns
    the parses it.

    :datadir: The directory containing the file
    :filename: The filename of the XML file
    :returns: The parsed representation of the XML files content

    """
    with open(join(datadir, filename), 'rb') as msg:
        res = musicbrainzngs.mbxml.parse_message(msg)
    return res
