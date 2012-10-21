import ast
import unittest

from stag.python_ast_parser import DefinitionVisitor

class DefinitionVisitorTests(unittest.TestCase):
    def test_function(self):
        source = '''
def foo():
    pass
        '''

        tree = ast.parse(source)
        v = DefinitionVisitor()
        v.visit(tree)
        self.assertIn(
            ('foo', 2),
            v.definitions)

    def test_class(self):
        source='''
class Foo:
        pass
        '''
        tree = ast.parse(source)
        v = DefinitionVisitor()
        v.visit(tree)
        self.assertIn(
            ('Foo', 2),
            v.definitions)