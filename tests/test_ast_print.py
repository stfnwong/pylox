# modules under test
from tools.ast_print import ASTPrint
from loxpy.expr import BinaryExpr, LiteralExpr
from loxpy.token import Token, TokenType



def test_parenthesize():
    # expr is "2 + 4"
    left      = Token(TokenType.NUMBER, '2', 2.0, 1)
    op        = Token(TokenType.PLUS, '+', None, 1)
    right     = Token(TokenType.NUMBER, '4', 4.0, 1)
    test_expr = BinaryExpr(op, LiteralExpr(left), LiteralExpr(right))
    ast_print = ASTPrint()

    ast_string = ast_print.print(test_expr)
    exp_string = "(+ 2 4)"

    assert ast_string == exp_string
