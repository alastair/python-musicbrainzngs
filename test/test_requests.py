import unittest
import os
import sys
import time
sys.path.append(os.path.abspath(".."))
from musicbrainzngs import musicbrainz
from test._common import Timecop


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

    def test_second_rapid_query_waits(self):
        self.func()
        time1 = time.time()
        self.func()
        time2 = time.time()
        self.assertGreaterEqual(time2 - time1, 1.0)

    def test_second_distant_query_does_not_wait(self):
        self.func()
        time.sleep(1.0)
        time1 = time.time()
        self.func()
        time2 = time.time()
        self.assertAlmostEqual(time1, time2)

class BatchedRateLimitingTest(unittest.TestCase):
    def setUp(self):
        musicbrainz.limit_requests = 3
        musicbrainz.limit_interval = 3.0

        self.cop = Timecop()
        self.cop.install()

        @musicbrainz._rate_limit
        def limited():
            pass
        self.func = limited

    def tearDown(self):
        musicbrainz.limit_requests = 1
        musicbrainz.limit_interval = 1.0

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
        self.assertGreaterEqual(time2 - time1, 1.0)
