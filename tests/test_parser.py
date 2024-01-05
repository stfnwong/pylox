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
WHILE_PROGRAM = "programs/while.lox"
FOR_PROGRAM = "programs/for.lox"


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


def test_parse_while() -> None:
    source = load_source(WHILE_PROGRAM)
    parsed_output = parse_input(source)

    # We expect one VarStmt, one WhileStmt, one PrintStmt
    exp_types = [VarStmt, WhileStmt, PrintStmt]
    assert len(parsed_output) == len(exp_types)

    for p, t in zip(parsed_output, exp_types):
        assert type(p) == t


def test_parse_for() -> None:
    source = load_source(FOR_PROGRAM)
    parsed_output = parse_input(source)

    # For loops with an initializer will be parsed into a single block statement.
    # The second for loop will be parsed into a WhileStmt
    exp_types = [BlockStmt, WhileStmt]
    assert len(parsed_output) == len(exp_types)
    
    for p, t in zip(parsed_output, exp_types):
        assert type(p) == t

    # Inside the first for loop we expect one variable statement 
    # for the initializer, and one while statment for the rest of the body.
    exp_loop_stmts_1 = [VarStmt, WhileStmt]
    assert len(parsed_output[0].stmts) == len(exp_loop_stmts_1)

    # Inside the second loop is a single WhileStmt
    assert isinstance(parsed_output[1], WhileStmt)
    # Note that the body of a BlockStmt has type Sequence[Stmt]
    assert isinstance(parsed_output[1].body, BlockStmt)
    assert isinstance(parsed_output[1].body.stmts[0], PrintStmt)

