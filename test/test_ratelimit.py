import unittest
import time
import musicbrainzngs
from musicbrainzngs import musicbrainz
from test._common import Timecop

import pytest


class RateLimitArgumentTest(unittest.TestCase):
    def test_invalid_args(self):
        """ Passing invalid arguments to set_rate_limit should throw
            an exception """
        try:
            musicbrainzngs.set_rate_limit(1, 0)
            self.fail("Required exception wasn't raised")
        except ValueError as e:
            self.assertTrue("new_requests" in str(e))

        try:
            musicbrainzngs.set_rate_limit(0, 1)
            self.fail("Required exception wasn't raised")
        except ValueError as e:
            self.assertTrue("limit_or_interval" in str(e))

        try:
            musicbrainzngs.set_rate_limit(1, -1)
            self.fail("Required exception wasn't raised")
        except ValueError as e:
            self.assertTrue("new_requests" in str(e))

        try:
            musicbrainzngs.set_rate_limit(0, -1)
            self.fail("Required exception wasn't raised")
        except ValueError as e:
            self.assertTrue("limit_or_interval" in str(e))

class RateLimitingTest(unittest.TestCase):
    def setUp(self):
        self.cop = Timecop()
        self.cop.install()

        @musicbrainz._rate_limit
        def limited():
            pass
        self.func = limited

    def tearDown(self):
        self.cop.restore()

    def test_do_not_wait_initially(self):
        time1 = time.time()
        self.func()
        time2 = time.time()
        self.assertAlmostEqual(time1, time2)

    @pytest.mark.xfail(reason="currently fails")
    def test_second_rapid_query_waits(self):
        """ Performing 2 queries should force a wait """
        self.func()
        time1 = time.time()
        self.func()
        time2 = time.time()
        self.assertTrue(time2 - time1 >= 1.0)

    def test_second_distant_query_does_not_wait(self):
        """ If there is a gap between queries, don't force a wait """
        self.func()
        time.sleep(1.0)
        time1 = time.time()
        self.func()
        time2 = time.time()
        self.assertAlmostEqual(time1, time2)

class BatchedRateLimitingTest(unittest.TestCase):
    def setUp(self):
        musicbrainzngs.set_rate_limit(3, 3)

        self.cop = Timecop()
        self.cop.install()

        @musicbrainz._rate_limit
        def limited():
            pass
        self.func = limited

    def tearDown(self):
        musicbrainzngs.set_rate_limit(1, 1)

        self.cop.restore()

    def test_initial_rapid_queries_not_delayed(self):
        time1 = time.time()
        self.func()
        self.func()
        self.func()
        time2 = time.time()
        self.assertAlmostEqual(time1, time2)

    def test_overage_query_delayed(self):
        time1 = time.time()
        self.func()
        self.func()
        self.func()
        self.func()
        time2 = time.time()
        self.assertTrue(time2 - time1 >= 1.0)

class NoRateLimitingTest(unittest.TestCase):
    """ Disable rate limiting """
    def setUp(self):
        musicbrainzngs.set_rate_limit(False)

        self.cop = Timecop()
        self.cop.install()

        @musicbrainz._rate_limit
        def limited():
            pass
        self.func = limited

    def tearDown(self):
        musicbrainzngs.set_rate_limit(True)

        self.cop.restore()

    def test_initial_rapid_queries_not_delayed(self):
        time1 = time.time()
        self.func()
        self.func()
        self.func()
        time2 = time.time()
        self.assertAlmostEqual(time1, time2)
