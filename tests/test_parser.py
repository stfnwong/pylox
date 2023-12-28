# Modules under test
from typing import List

from loxpy.parser import Parser
from loxpy.scanner import Scanner
from loxpy.token import Token, TokenType
from loxpy.expr import Expr, BinaryExpr, LiteralExpr
from loxpy.statement import Stmt, ExprStmt



def parse_input(expr_src: str) -> List[Stmt]:
    scanner       = Scanner(expr_src)
    token_list    = scanner.scan()
    parser        = Parser(token_list)
    parsed_output = parser.parse()

    return parsed_output


def test_simple_add() -> None:
    simple_expr = '2 + 2;'
    # Format the expected output
    token_left    = Token(TokenType.NUMBER, '2', float(2), 1)
    token_op      = Token(TokenType.PLUS, '', None, 1)
    token_right   = Token(TokenType.NUMBER, '2', float(2), 1)
    exp_output    = [ExprStmt(BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right)))]

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output

def test_simple_sub() -> None:
    simple_expr = '4 - 2;'
    # Format the expected output
    token_left    = Token(TokenType.NUMBER, '4', float(4), 1)
    token_op      = Token(TokenType.MINUS, '', None, 1)
    token_right   = Token(TokenType.NUMBER, '2', float(2), 1)
    exp_output    = [ExprStmt(BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right)))]

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output

def test_simple_mul() -> None:
    simple_expr = '4 * 4;'
    # Format the expected output
    token_left    = Token(TokenType.NUMBER, '4', float(4), 1)
    token_op      = Token(TokenType.STAR, '', None, 1)
    token_right   = Token(TokenType.NUMBER, '4', float(4), 1)
    exp_output    = [ExprStmt(BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right)))]

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output

def test_simple_div() -> None:
    simple_expr = '6 / 4;'
    # Format the expected output
    token_left    = Token(TokenType.NUMBER, '6', float(6), 1)
    token_op      = Token(TokenType.SLASH, '', None, 1)
    token_right   = Token(TokenType.NUMBER, '4', float(4), 1)
    exp_output    = [ExprStmt(BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right)))]

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output
