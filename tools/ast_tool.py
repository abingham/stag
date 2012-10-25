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
        self.last_line = None

    @property
    def indent(self):
        return '  ' * self.depth

    def get_source_line(self, node):
        try:
            line = linecache.getline(self.fname, node.lineno)
            if line == self.last_line:
                line = '.'
            else:
                self.last_line = line
            return line
        except AttributeError:
            return ''

    def show(self, node, *args):
        print('{:100}{}'.format(
            '{}[{}] {}'.format(
                self.indent,
                node.__class__.__name__.upper(),
                args),
            self.get_source_line(node).strip()))

    @recurse
    def visit_Call(self, node):
        self.show(node, node.func)

    @recurse
    def visit_Name(self, node):
        self.show(node, node.id)

    @recurse
    def visit_Attribute(self, node):
        self.show(node, node.attr)

    @recurse
    def generic_visit(self, node):
        self.show(node)

@baker.command
def tree(filename):
    with open(filename, 'r') as f:
        source = f.read()
    tree = ast.parse(source)
    TreeDump(filename).visit(tree)

if __name__ == '__main__':
    baker.run()