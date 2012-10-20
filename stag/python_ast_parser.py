import ast

class DefinitionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.definitions = []

    def visit_FunctionDef(self, node):
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.generic_visit(node)

class Parser:
    def __init__(self):
        self._fname = None
        self._ast = None

    @property
    def ast(self):
        if self._ast is None:
            assert self.fname is not None, 'set_file() must be called before rebuilding AST.'

            with open(self.fname) as f:
                source = f.read()

            self.ast = ast.parse(source, filename=self.fname)

    @property
    def fname(self):
        return self._fname

    def set_file(self, fname):
        self._fname = fname
        self._ast = None

    def definitions(self):
