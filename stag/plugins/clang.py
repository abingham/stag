from stag.parser.clang_parser import Parser

class Plugin:
    @property
    def name(self):
        return 'stag_clang'

    def patterns(self):
        return [
            '.*\.cpp',
            '.*\.cc',
            '.*\.cxx',
            '.*\.c',
            '.*\.hpp',
            '.*\.h',
            '.*\.hxx',
        ]

    def create_parser(self):
        return Parser()
