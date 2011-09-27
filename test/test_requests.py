import unittest
import os
import sys
import time
sys.path.append(os.path.abspath(".."))
import musicbrainz
from test._common import Timecop

@musicbrainz._rate_limit
def limited():
    pass

class RateLimitingTest(unittest.TestCase):
    def setUp(self):
        limited.last_call = 0.0
        self.cop = Timecop()
        self.cop.install()

    def tearDown(self):
        self.cop.restore()

    def test_do_not_wait_initially(self):
        time1 = time.time()
        limited()
        time2 = time.time()
        self.assertAlmostEqual(time1, time2)

    def test_second_rapid_query_waits(self):
        limited()
        time1 = time.time()
        limited()
        time2 = time.time()
        self.assertGreaterEqual(time2 - time1, 1.0)

    def test_second_distant_query_does_not_wait(self):
        limited()
        time.sleep(1.0)
        time1 = time.time()
        limited()
        time2 = time.time()
        self.assertAlmostEqual(time1, time2)
