from typing import Sequence

from loxpy.expr import BinaryExpr, LiteralExpr, UnaryExpr
from loxpy.statement import Stmt, ExprStmt, PrintStmt
from loxpy.token import Token, TokenType
from loxpy.scanner import Scanner
from loxpy.parser import Parser
from loxpy.interpreter import Interpreter
from loxpy.util import load_source, float_equal


GLOBAL_VERBOSE = False

WHILE_PROGRAM = "programs/while.lox"


def parse_input(expr_src: str) -> Sequence[Stmt]:
    scanner       = Scanner(expr_src)
    token_list    = scanner.scan()
    parser        = Parser(token_list)
    parsed_output = parser.parse()

    return parsed_output



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

    tok_string = Token(TokenType.STRING, "bet you can't print this", None, 1)
    stmts = [PrintStmt(LiteralExpr(tok_string))]

    ret = interp.interpret(stmts)
    assert len(ret) == 1
    assert ret[0] == tok_string


def test_interpret_while() -> None:
    source = load_source(WHILE_PROGRAM)
    stmts = parse_input(source)

    interp = Interpreter(verbose=GLOBAL_VERBOSE)
    interp.interpret(stmts)

    expected_state = {"i": 10.0}
    for var_name in expected_state:
        assert var_name in interp.environment.values
        assert interp.environment.values[var_name] == expected_state[var_name]


def test_interpret_fib_for() -> None:
    source = load_source("programs/fib_for.lox")
    stmts = parse_input(source)
    interp = Interpreter(verbose=GLOBAL_VERBOSE)
    interp.interpret(stmts)

    expected_state = {"a": 1597.0, "temp": 987.0}
    for var_name in expected_state:
        assert var_name in interp.environment.values
        assert interp.environment.values[var_name] == expected_state[var_name]
