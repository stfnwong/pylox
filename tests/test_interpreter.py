from typing import Sequence

from loxpy.expr import BinaryExpr, LiteralExpr, UnaryExpr
from loxpy.statement import Stmt, ExprStmt
from loxpy.token import Token, TokenType
from loxpy.scanner import Scanner
from loxpy.parser import Parser
from loxpy.interpreter import Interpreter
from loxpy.util import float_equal


GLOBAL_VERBOSE = True


#def load_source(filename: str) -> str:
#    with open(filename, 'r') as fp:
#        source = fp.read()
#    return str(source)
#



def test_interpret_unary() -> None:
    interp = Interpreter(verbose=GLOBAL_VERBOSE)

    tok_num1 = Token(TokenType.NUMBER, "2", None, 1)
    tok_minus  = Token(TokenType.MINUS, "-", None, 1)
    expr = [ExprStmt(UnaryExpr(tok_minus, LiteralExpr(tok_num1)))]

    value = interp.interpret(expr)
    exp_value = -2.0

    assert float_equal(value[0], exp_value)


def test_interpret_binary() -> None:
    interp = Interpreter(verbose=GLOBAL_VERBOSE)

    tok_num1 = Token(TokenType.NUMBER, "2", None, 1)
    tok_mul  = Token(TokenType.STAR, "*", None, 1)
    tok_num2 = Token(TokenType.NUMBER, "4", None, 1)

    expr     = [ExprStmt(BinaryExpr(tok_mul, LiteralExpr(tok_num1), LiteralExpr(tok_num2)))]
    value = interp.interpret(expr)
    exp_value = 8.0

    assert float_equal(value[0], exp_value)


# TODO: place a grouping expression on one side of a binary expression
#def test_interpret_nested_binary() -> None:
#    interp = Interpreter(verbose=GLOBAL_VERBOSE)
#
#    # Inner expr
#    inner_num1 = Token(TokenType.NUMBER, "2", None, 1)
#    inner_mul  = Token(TokenType.STAR, "*", None, 1)
#    inner_num2 = Token(TokenType.NUMBER, "4", None, 1)
#    inner_expr = BinaryExpr(inner_mul, LiteralExpr(inner_num1), LiteralExpr(inner_num2))
#
#    outer_num1 = Token(TokenType.NUMBER, "10", None, 1)
#    outer_mul  = Token(TokenType.STAR, "*", None, 1)
#    outer_expr = ExprStmt(BinaryExpr(outer_mul, inner_expr, LiteralExpr(outer_num1)))
#
#    #from pudb import set_trace; set_trace()
#    value = interp.interpret([outer_expr])
#
#    exp_value = 80.0
#
#    assert float_equal(value[0], exp_value)
#

def test_interpret_print() -> None:
    interp = Interpreter(verbose=GLOBAL_VERBOSE)

    tok_print = Token(TokenType.PRINT, "print", None, 1)
    tok_string = Token(TokenType.STRING, "bet you can't print this", None, 1)
