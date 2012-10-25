import ast
import unittest

from stag.parser.python_ast_parser import Visitor

def parse(source):
    """Parse `source`, visit it with a Visitor, and return that
    Visitor.

    """
    tree = ast.parse(source)
    v = Visitor()
    v.visit(tree)
    return v

class ReferenceTests(unittest.TestCase):
    """Reference-detection tests."""
    def test_simple_function(self):
        v = parse(
            '''
x = llama(a)
            ''')

    def test_lambda(self):
        v = parse(
            '''
x = lambda y: y + 1
x(3)
            ''')

        self.assertIn(
            ('x', 3),
            v.references)

    def test_class_reference(self):
        v = parse(
            '''
class Llama:
  pass

y = Llama()
            ''')

        self.assertIn(
            ('Llama', 5),
            v.references)

    def test_method_reference(self):
        v = parse('''
y = foo.bar(yak)
                  ''')
        self.assertIn(
            ('bar', 2),
            v.references)

class DefinitionTests(unittest.TestCase):
    """Definition-detection tests."""
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