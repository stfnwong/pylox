"""
ASTPRINT
In the original this is part of the lox package, but
I don't think I will use this as anything other than a
tool.

TODO : Add graphviz support

"""

from typing import List

from loxpy.expr import (
    Expr,
    BinaryExpr,
    LiteralExpr,
    GroupingExpr,
    UnaryExpr
)



class ASTPrint:
    """
    Visitor which prints an AST in human-readable format
    """

    def _parenthesize(self, name: str, expr_list: List[Expr]):

        s = []
        s.append(f"({name}")
        for e in expr_list:
            s.append(" ")
            # The 'pythonic' way to deal wth subclassing
            try:
                ea = e.accept(self)
            except:
                continue
            s.append(f"{ea}")
            #s.append(f"{repr(ea)}")
        s.append(")")

        return ''.join(s)

    def visit_binary_expr(self, expr: BinaryExpr) -> str:
        return self._parenthesize(expr.op.lexeme, [expr.left, expr.right])

    def visit_grouping_expr(self, expr: GroupingExpr) -> str:
        return self._parenthesize("group", [expr.expression])

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr):
        return self._parenthesize(expr.op.lexeme, [expr.right])

    # TODO : remove this
    def visit(self, expr: Expr):

        if type(expr) is BinaryExpr:
            self.visit_binary_expr(expr)
        elif type(expr) is GroupingExpr:
            self.visit_grouping_expr(expr)
        elif type(expr) is LiteralExpr:
            self.visit_literal_expr(expr)
        elif type(expr) is UnaryExpr:
            self.visit_unary_expr(expr)
        else:
            raise ValueError(f"Unknown expression {expr} with type {type(expr)}")

    def print(self, expr: Expr) -> str:
        return expr.accept(self)

