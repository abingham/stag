class Parser:
    """A parser for C/C++ code which uses an external clang-based
    tool.

    This is obviously still a work in progress...nothing to see here...

    """

    def __init__(self):
        self._fname = None

    @property
    def fname(self):
        return self._fname

    def set_file(self, fname):
        self._fname = fname

    def definitions(self):
        assert self._fname is not None

        result = subprocess.check_output(
            ["echo", "someFunction 42"],
            universal_newline=True)

        for r in result.split('\n'):
            name, lineno = r.split()
            yield name, int(lineno)
