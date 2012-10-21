import os
import unittest

# from stag import app

class Tests(unittest.TestCase):
    def setUp(self):
        self.fname = 'test.sqlite'

    def tearDown(self):
        try:
            os.remove(self.fname)
        except OSError:
            pass

    @unittest.skip('strange import error...')
    def test_scan_defs(self):
        stag.app.scan_definitions_command(
            os.path.join(
                os.path.split(__file__)[0],
                '..'),
            self.fname)