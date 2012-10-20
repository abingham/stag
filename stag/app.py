import os
import sqlite

import baker

# TODO: Use ABC for IndexStorage?

def consume(iter):
    for _ in iter: pass

class IndexStorage:
    "Interface definition for index storage."
    def clear_defs(self):
        "Clear out storage."
        pass

    def add_def(self, name, filename, lineno):
        "Add a new definition."
        pass

    def __enter__(self):
        pass

    def __exit__(self, t, b, tb):
        pass

class Sqlite3Storage:
    def __init__(self, filename):
        self.filename = filename

    def clear_defs(self):
        pass

    def add_def(self, name, filename, lineno):
        pass

    def __enter__(self):
        self.conn = sqlite3.connet(self.filename)

    def __exit__(self, t, v, tb):
        self.conn.close()

class Scanner:
    def __init__(self, storage, parser_map):
        self.storage = storage
        self.parser_map = parser_map

    def find_parser(self, fname):
        for pattern, parser in self.parser_map.items():
            if re.match(pattern, fname):
                return parser

    def scan_defs(self, dirpath, dirnames, filenames):
        for fname in filenames:
            parser = self.find_parser(fname)
            if parser:
                parser.set_file(fname)
                for name, lineno in parser.definitions():
                    self.storage.add_def(name, fname, lineno)

@baker.command(name='scan_defs')
def scan_definitions_command(dir, filename):
    with Sqlite3Storage(filename) as storage:
        scanner = Scanner(storage)
        storage.clear_defs()
        consume(map(scanner.scan_defs, os.walk(dir)))