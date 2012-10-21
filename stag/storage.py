import sqlite3

# TODO: Use ABC for IndexStorage?

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

class PrintStorage:
    def clear_defs(self):
        pass

    def add_def(self, name, filename, lineno):
        print('{}:{}: {}'.format(filename, lineno, name))

    def __enter__(self):
        return self

    def __exit__(self, t, b, tb):
        pass

class Sqlite3Storage:
    def __init__(self, filename):
        self.filename = filename
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.filename)

    def close(self):
        self.conn.close()

    def clear_defs(self):
        pass

    def add_def(self, name, filename, lineno):
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, t, v, tb):
        self.close()
