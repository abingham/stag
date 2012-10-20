import ast
import unittest

from stag.python_ast_parser import DefinitionVisitor

class DefinitionVisitorTests(unittest.TestCase):
    def test_functions(self):
        source = '''
def foo():
    pass
        '''

        tree = ast.parse(source)
        v = DefinitionVisitor()
        v.visit(tree)