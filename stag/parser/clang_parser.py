"""Provides a clang-based C/C++ parser.
"""

import subprocess

class Parser:
    """A parser for C/C++ code which uses an external clang-based
    tool.

    This is obviously still a work in progress...nothing to see here...

    """

    def __init__(self):
        self._fname = None

    @property
    def fname(self):
        """The filename being parsed."""
        return self._fname

    def set_file(self, fname):
        """Set the filename to be parsed.

        Args:
          fname: A file name.

        """

        self._fname = fname

    def definitions(self):
        """Generate the definitions in ``self.fname``.

        """

        assert self._fname is not None

        result = subprocess.check_output(
            ["echo", "someFunction 42"],
            universal_newline=True)

        for refn in result.split('\n'):
            name, lineno = refn.split()
            yield name, int(lineno)
