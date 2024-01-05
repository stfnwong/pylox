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
    UnaryExpr,
    VarExpr
)



class ASTPrinter:
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

    def visit_literal_expr(self, expr: LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: UnaryExpr):
        return self._parenthesize(expr.op.lexeme, [expr.right])

    def visit_var_expr(self, expr: VarExpr) -> str:
        pass

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
        return str(expr.accept(self))



# Example AST from book
if __name__ == "__main__":
    from loxpy.token import Token, TokenType

    expr = BinaryExpr(
        Token(TokenType.STAR, "*", None, 1),
        UnaryExpr(
            Token(TokenType.MINUS, "-", None, 1),
            LiteralExpr(Token(TokenType.NUMBER, "123", 123, 1))
        ),
        GroupingExpr(
            LiteralExpr(Token(TokenType.NUMBER, "45.67", 45.67, 1))
        )
    )

    printer = ASTPrinter()
    print(printer.print(expr))
