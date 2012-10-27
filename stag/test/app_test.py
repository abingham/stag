import os
import unittest

from stag import app

class Tests(unittest.TestCase):
    def setUp(self):
        self.fname = 'test.sqlite'

    def tearDown(self):
        try:
            os.remove(self.fname)
        except OSError:
            pass

    def test_scan_defs(self):
        app.scan_command(
            os.path.join(
                os.path.split(__file__)[0],
                '..'),
            self.fname)