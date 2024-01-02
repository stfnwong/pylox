# Modules under test
from typing import Sequence
import pytest

from loxpy.util import load_source
from loxpy.error import LoxParseError
from loxpy.parser import Parser
from loxpy.scanner import Scanner
from loxpy.token import Token, TokenType
from loxpy.expr import BinaryExpr, LiteralExpr
from loxpy.statement import (
    Stmt, 
    BlockStmt, 
    ExprStmt, 
    PrintStmt, 
    VarStmt, 
    WhileStmt
)


BLOCK_PROGRAM = "programs/shadow.lox"
ITER_PROGRAM = "programs/iter.lox"


def parse_input(expr_src: str) -> Sequence[Stmt]:
    scanner       = Scanner(expr_src)
    token_list    = scanner.scan()
    parser        = Parser(token_list)
    parsed_output = parser.parse()

    return parsed_output


def test_raise_parse_error() -> None:
    source = "print 1"    # No trailing semicolon should raise LoxParseError
    scanner       = Scanner(source)
    token_list    = scanner.scan()
    parser        = Parser(token_list)

    with pytest.raises(LoxParseError):
        parser.parse()


def test_simple_add() -> None:
    simple_expr = "2 + 2;"
    # Format the expected output
    token_left    = Token(TokenType.NUMBER, "2", float(2), 1)
    token_op      = Token(TokenType.PLUS, "+", None, 1)
    token_right   = Token(TokenType.NUMBER, "2", float(2), 1)
    exp_output    = [ExprStmt(BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right)))]

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output


def test_simple_sub() -> None:
    simple_expr = "4 - 2;"
    # Format the expected output
    token_left    = Token(TokenType.NUMBER, "4", float(4), 1)
    token_op      = Token(TokenType.MINUS, "-", None, 1)
    token_right   = Token(TokenType.NUMBER, "2", float(2), 1)
    exp_output    = [ExprStmt(BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right)))]

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output


def test_simple_mul() -> None:
    simple_expr = "4 * 4;"
    # Format the expected output
    token_left    = Token(TokenType.NUMBER, "4", float(4), 1)
    token_op      = Token(TokenType.STAR, "*", None, 1)
    token_right   = Token(TokenType.NUMBER, "4", float(4), 1)
    exp_output    = [ExprStmt(BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right)))]

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output


def test_simple_div() -> None:
    simple_expr = "6 / 4;"
    # Format the expected output
    token_left    = Token(TokenType.NUMBER, "6", float(6), 1)
    token_op      = Token(TokenType.SLASH, "/", None, 1)
    token_right   = Token(TokenType.NUMBER, "4", float(4), 1)
    exp_output    = [ExprStmt(BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right)))]

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output



def test_parse_logic() -> None:
    pass


# TODO: write a test that exercises _synchronise()



def test_parse_block() -> None:
    source = load_source(BLOCK_PROGRAM)
    parsed_output = parse_input(source)

    # SHould be 7 statements - 3 var, one block, 3 print
    assert len(parsed_output) == 7

    exp_types = [VarStmt, VarStmt, VarStmt, BlockStmt, PrintStmt, PrintStmt, PrintStmt]

    for p, t in zip(parsed_output, exp_types):
        assert type(p) == t

    # TODO: Anything else worth testing?


def test_parse_iter() -> None:
    source = load_source(ITER_PROGRAM)
    parsed_output = parse_input(source)

    # We expect one VarStmt, one WhileStmt
    assert len(parsed_output) == 2
    
    exp_types = [VarStmt, WhileStmt]
    for p, t in zip(parsed_output, exp_types):
        assert type(p) == t
