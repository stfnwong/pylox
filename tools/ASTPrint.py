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

from loxpy import Expression
# Debug
#from pudb import set_trace; set_trace()

class ASTPrint(object):
    def __init__(self):
        pass

    def _parenthesize(self, name, expr_list):

        if type(expr_list) is not list:
            raise TypeError('expr_list must be a list')

        s = []
        s.append('(')
        for e in expr_list:
            s.append(' ')
            # The 'pythonic' way to deal wth subclassing
            try:
                ea = e.accept(self)
            except:
                continue
            s.append(str(ea))
        s.append(')')

        return ''.join(s)

    def visit_binary_expr(self, expr):
        return self._parenthesize(expr.op.lexeme, [expr.left, expr.right])

    def visit_grouping_expr(self, expr):
        return self._parenthesize("group", [expr.expression])

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr):
        return self._parenthesize(expr.op.lexeme, [expr.right])

    # TODO : remove this
    def visit(self, expr):

        if type(expr) is Expression.Binary:
            self.visit_binary_expr(expr)
        elif type(expr) is Expression.Grouping:
            self.visit_grouping_expr(expr)
        elif type(expr) is Expression.Literal:
            self.visit_literal_expr(expr)
        elif type(expr) is Expression.Unary:
            self.visit_unary_expr(expr)
        else:
            raise ValueError('Invalid expression type %s' % type(expr))

    # TODO : visit all the methods
    def ast_print(self, expr):
        return expr.accept(self)




if __name__ == '__main__':
    ast_print = ASTPrint()
    #ast_print.ast_print()
