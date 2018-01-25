"""
ASTPRINT
In the original this is part of the lox package, but
I don't think I will use this as anything other than a
tool.

TODO : Add graphviz support

Stefan Wong 2018
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ASTPrint(object):
    def __init__(self):
        pass

    def _parenthesize(self, name, expr_list):
        if type(expr_list) is not list:
            raise ValueError('expr_list must be a list')

        s = []
        s.append('(')
        for e in expr_list:
            s.append(' ')
            ea = e.accept(self)
            s.append(str(ea))
        s.append(')')

        return ''.join(s)

    def visit_binary_expr(self, expr):
        return self._parenthesize(expr.op.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr):
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr):
        return self._parenthesize(expr.op.lexeme, expr.right)


    # TODO : visit all the methods
    def ast_print(self, expr):
        return expr.accept(self)



if __name__ == '__main__':
    ast_print = ASTPrint()
    #ast_print.ast_print()
