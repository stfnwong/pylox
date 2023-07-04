# modules under test
from tools import ASTPrint
from loxpy import Expression, Token


def test_parenthesize():
    #verbose = True
    test_expr = '2 + 2;'

    left      = Token.Token(Token.NUMBER, '2', 2.0, 1)
    op        = Token.Token(Token.PLUS, '', None, 1)
    right     = Token.Token(Token.NUMBER, '4', 4.0, 1)
    test_expr = Expression.Binary(left, op, right)
    expr_list = [test_expr]
    ast_print = ASTPrint.ASTPrint()
    ast_string = ast_print.ast_print(test_expr)
    #ast_string = ast_print._parenthesize('expr', expr_list)

    print(ast_string)
    # TODO: add canonical example string 

