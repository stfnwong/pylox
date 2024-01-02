"""
ASTGraph
Create a graph of the AST with graphviz

"""


from typing import Sequence
from loxpy.expr import Expr


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

    def _gen_node(self, name: str, expr_list: Sequence[Expr]):
        pass

    def visit_literal_expr(self, expr: Expr):
        s = f"Node{self.ncount} [label={str(type(expr))}]"
        self.ncount += 1
        self.dot_body.append(s)

    def visit_unary_expr(self, expr: Expr):
        s = f"Node{self.ncount} [label={str(type(expr))}]"
        self.ncount += 1
        self.dot_body.append(s)

    def visit_binary_expr(self, expr: Expr):
        s = f"Node{self.ncount} [label={str(type(expr))}]"
        self.ncount += 1
        self.dot_body.append(s)

