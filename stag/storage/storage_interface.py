# TODO: Use ABC for IndexStorage?

class IndexStorage:
    "Interface definition for index storage."

    def connect(self):
        "Connect to low-level storage."
        pass

    def close(self):
        "Close connection to low-level storage."
        pass

    def clear_defs(self):
        "Clear out storage."
        pass

    def add_def(self, name, filename, lineno, source):
        "Add a new definition."
        pass

    def definitions(self):
        """Get iterable of all definitions in storage.

        Each definitions is a tuple of the form:

          (definition-name, filename, lineno, source).

        """
        pass

    def find_definitions(self, name):
        """Get all definitions for a given name.

        Each definitions is a tuple of the form:

          (definition-name, filename, lineno, source).

        """
        pass

    def add_ref(self, name, filename, lineno, source):
        "Add a new reference."
        pass

    def references(self):
        """Get iterable of all references in storage.

        Each reference is a tuple of the form:

          (reference-name, filename, lineno, source).
        """
        pass

    def find_references(self, name):
        """Get all references to a given name.

        Each reference is a tuple of the form:

          (reference-name, filename, lineno, source).

        """
        pass
