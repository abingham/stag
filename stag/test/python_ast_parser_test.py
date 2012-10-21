import ast
import unittest

from stag.python_ast_parser import DefinitionVisitor

def parse(source):
    tree = ast.parse(source)
    v = DefinitionVisitor()
    v.visit(tree)
    return v

class DefinitionVisitorTests(unittest.TestCase):
    def test_function(self):
        v = parse(
            '''
def foo():
  pass
            ''')
        self.assertIn(
            ('foo', 2),
            v.definitions)

    def test_class(self):
        v = parse('''
class Foo:
        pass
        ''')
        self.assertIn(
            ('Foo', 2),
            v.definitions)

    def test_method(self):
        v = parse('''
class Foo:
  def bar(self):
     pass
        ''')
        self.assertIn(
            ('Foo.bar', 3),
            v.definitions)

    def test_method_and_func(self):
        v = parse('''
def func1(): pass
class Foo:
  def meth1(self): pass
def func2(): pass
        ''')

        defs = (
            ('func1', 2),
            ('Foo', 3),
            ('Foo.meth1', 4),
            ('func2', 5))

        for d in defs:
            self.assertIn(
                d,
                v.definitions)

    def test_nested_class_method(self):
        v = parse('''
class Foo:
  class Bar:
    def baz(self): pass
''')
        defs = (
            ('Foo', 2),
            ('Foo.Bar', 3),
            ('Foo.Bar.baz', 4),
            )
        for d in defs:
            self.assertIn(
                d,
                v.definitions)