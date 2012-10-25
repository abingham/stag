import ast
import decorator
import linecache

import baker

@decorator.decorator
def recurse(f, self, node):
    f(self, node)
    self.depth += 1
    ast.NodeVisitor.generic_visit(self, node)
    self.depth -= 1

class TreeDump(ast.NodeVisitor):
    def __init__(self, filename):
        self.fname = filename
        self.depth = 0

    @property
    def indent(self):
        return '  ' * self.depth

    def get_source_line(self, node):
        try:
            return linecache.getline(self.fname, node.lineno)
        except AttributeError:
            return ''

    def show(self, node_type, node, *args):
        print('{:100}{}'.format(
            '{}[{}] {}'.format(self.indent, node_type.upper(), args),
            self.get_source_line(node).strip()))

    @recurse
    def visit_Call(self, node):
        self.show('call', node, node.func)

    @recurse
    def visit_Name(self, node):
        self.show('name', node, node.id)

    @recurse
    def visit_Attribute(self, node):
        self.show('attribute', node, node.attr)

    @recurse
    def generic_visit(self, node):
        self.show(node.__class__.__name__, node)

@baker.command
def tree(filename):
    with open(filename, 'r') as f:
        source = f.read()
    tree = ast.parse(source)
    TreeDump(filename).visit(tree)

if __name__ == '__main__':
    baker.run()