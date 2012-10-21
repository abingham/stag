import logging
import sqlite3

log = logging.getLogger(__file__)

# TODO: Use ABC for IndexStorage?

class IndexStorage:
    "Interface definition for index storage."
    def clear_defs(self):
        "Clear out storage."
        pass

    def add_def(self, name, filename, lineno):
        "Add a new definition."
        pass

    def definitions(self):
        "Get iterable of all definitions in storage."
        pass

    def find_definitions(self, name):
        "Get all definitions for a given name."
        pass

    def __enter__(self):
        pass

    def __exit__(self, t, b, tb):
        pass

class Sqlite3Storage:
    def __init__(self, filename):
        self.filename = filename
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.filename)
            self.conn.row_factory = sqlite3.Row
            self.conn.isolation_level = 'EXCLUSIVE'
            cur = self.conn.cursor()
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS definitions
                (name text, filename text, lineno int)''')
            cur.execute(
                'CREATE INDEX IF NOT EXISTS name_index ON definitions(name)')

    def close(self):
        self.conn.commit()
        self.conn.close()

    def clear_defs(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM definitions')

    def add_def(self, name, filename, lineno):
        log.info(
            'Sqlite3Storage.add_def(name={}, filename={}, lineno={})'.format(
                name, filename, lineno))

        cur = self.conn.cursor()
        cur.execute('INSERT INTO definitions VALUES(?,?,?)',
                    (name, filename, lineno))

    def definitions(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM definitions')
        for row in cur:
            yield (row['name'], row['filename'], row['lineno'])

    def find_definitions(self, name):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM definitions WHERE name=?',
                    (name,))
        for row in cur:
            yield (row['name'], row['filename'], row['lineno'])

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, t, v, tb):
        self.close()
