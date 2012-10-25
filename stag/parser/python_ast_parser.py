import ast

class Visitor(ast.NodeVisitor):
    """An ast.NodeVisitor that gathers information about function and
    class definitions.

    """

    def __init__(self):
        self.classes = []
        self.definitions = []
        self.references = []
        self.current_call = None

    def visit_FunctionDef(self, node):
        func_name = '.'.join(self.classes + [node.name])
        self.definitions.append((func_name, node.lineno))
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        class_name = '.'.join(self.classes + [node.name])
        self.definitions.append((class_name, node.lineno))
        self.classes.append(node.name)
        self.generic_visit(node)
        self.classes = self.classes[:-1]

    def visit_Call(self, node):
        self.current_call = node
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if self.current_call:
            self.references.append((node.attr, node.lineno))
            self.current_call = None
        self.generic_visit(node)

    def visit_Name(self, node):
        if self.current_call:
            self.references.append((node.id, node.lineno))
            self.current_call = None
        self.generic_visit(node)

class Parser:
    """A parser for Python source code which uses the `ast` module."""

    def __init__(self):
        self._fname = None
        self._ast = None
        self._visitor = None

    @property
    def ast(self):
        if self._ast is None:
            assert self.fname is not None, 'set_file() must be called before rebuilding AST.'

            with open(self.fname) as f:
                source = f.read()

            self._ast = ast.parse(source, filename=self.fname)
        return self._ast

    @property
    def visitor(self):
        if self._visitor is None:
            self._visitor = Visitor()
            self._visitor.visit(self.ast)
        return self._visitor

    @property
    def fname(self):
        return self._fname

    def set_file(self, fname):
        self._fname = fname
        self._ast = None
        self._visitor = None

    def definitions(self):
        return iter(self.visitor.definitions)

    def references(self):
        return iter(self.visitor.references)