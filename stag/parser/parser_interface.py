class Parser:
    "Interface definition for parsers."

    def set_file(self, fname):
        """Set the file on which the parser operates.

        This will be called multpile times with different
        files. Subsequent calls to get symbol locations should operate
        against the file set here.

        """
        pass

    def definitions(self):
        "Get iterable of definition tuples (symbol, lineno)."
        pass

    def references(self):
        "Get an iterable of reference tuples (symbol, lineno)."
        pass