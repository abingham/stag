import os
import unittest

from stag.storage.manager import StorageManager
from stag.storage.sqlalchemy_storage import SqlAlchemyStorage

class Tests(unittest.TestCase):
    def setUp(self):
        self.fname = 'test.sqlite'

    def tearDown(self):
        try:
            os.remove(self.fname)
        except OSError:
            pass

    def test_construction(self):
        s = SqlAlchemyStorage(self.fname)

    def _populate(self, s):
        values = [
            ('foo', 'sample/bar.py', 1, 'some source code foo'),
            ('llama', 'cool/stuff/animal.py', 42, 'some source code llama'),
            ('DeathStar', 'empire/fleet/space_stations.cpp', 421, 'some source code DeathStar'),
        ]


        self.assertEqual(
            len(list(s.definitions())), 0)

        for v in values:
            s.add_def(*v)

        self.assertEqual(
            len(list(s.definitions())), len(values))

        for d in s.definitions():
            self.assertIn(d, values)

    def test_add_def(self):
        with StorageManager(SqlAlchemyStorage(self.fname)) as s:
            self._populate(s)

    def test_clear_defs(self):
        with StorageManager(SqlAlchemyStorage(self.fname)) as s:
            self._populate(s)
            s.clear_defs()
            self.assertEqual(
                len(list(s.definitions())), 0)