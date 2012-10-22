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
