from stag.parser.python_ast_parser import Parser

class Plugin:
    @property
    def name(self):
        return 'stag_python'

    def patterns(self):
        return [
            '.*\.py',
            # TODO: pyx? SConstruct/script?
        ]

    def create_parser(self):
        return Parser()
