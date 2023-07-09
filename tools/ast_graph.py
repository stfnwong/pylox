"""
ASTGraph
Create a graph of the AST with graphviz

Stefan Wong 2018
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from loxpy import Expression

class ASTGraph(object):
    def __init__(self):
        self.dot_header = """\
            digraph astgraph { \
            node [shape=circle, fontsize=12.0, fontname="Courier", \
            height=.1];\
            ranksep=.3; \
            edge [arrowsize=.5]
        """
        self.dot_body = []
        self.ncount = 1

    def _gen_node(self, name, expr_list):
        pass

    def visit_literal_expr(self, expr):
        s = 'node%d [label="%s"]\n' % (self.ncount, str(type(expr)))
        self.ncount += 1
        self.dot_body.append(s)

    def visit_unary_expr(self, expr):
        s = 'node%d [label="%s"]\n' % (self.ncount, str(type(expr)))
        self.ncount += 1
        self.dot_body.append(s)

    def visit_binary_expr(self, expr):
        s = 'node%d [label="%s"]\n' % (self.ncount, str(type(expr)))
        self.ncount += 1

