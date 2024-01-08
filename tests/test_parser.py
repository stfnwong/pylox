# Modules under test
from typing import Sequence
import pytest

from loxpy.util import load_source
from loxpy.error import LoxParseError
from loxpy.parser import Parser
from loxpy.scanner import Scanner
from loxpy.token import Token, TokenType
from loxpy.expr import AssignmentExpr, BinaryExpr, CallExpr, GetExpr, SetExpr, LiteralExpr
from loxpy.statement import (
    Stmt, 
    BlockStmt, 
    ClassStmt,
    ExprStmt, 
    FuncStmt,
    PrintStmt, 
    VarStmt, 
    WhileStmt
)


VAR_AND_OP_PROGRAM = "programs/op.lox"
BLOCK_PROGRAM = "programs/shadow.lox"
WHILE_PROGRAM = "programs/while.lox"
FOR_PROGRAM = "programs/for.lox"
FIB_FOR_PROGRAM = "programs/fib_for.lox"
FIB_FUNC_PROGRAM = "programs/fib_func.lox"
FUNC_PROGRAM = "programs/func1.lox"
CLASS_FIELDS_PROGRAM = "programs/class_fields.lox"
CLASS_THIS_PROGRAM = "programs/class_this.lox"


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


def test_var_and_op() -> None:
    source = load_source(VAR_AND_OP_PROGRAM)
    parsed_output = parse_input(source)

    exp_types = [VarStmt, VarStmt, VarStmt]
    assert len(parsed_output) == len(exp_types)

    for p, t in zip(parsed_output, exp_types):
        assert type(p) == t

    # The last statement should have a BinaryExpr as its initializer
    assert isinstance(parsed_output[2].initializer, BinaryExpr)




def test_simple_add() -> None:
    simple_expr = "2 + 2;"
    token_left    = Token(TokenType.NUMBER, "2", float(2), 1, 2)
    token_op      = Token(TokenType.PLUS, "+", None, 1, 4)
    token_right   = Token(TokenType.NUMBER, "2", float(2), 1, 6)
    exp_output    = [ExprStmt(BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right)))]

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output


def test_simple_sub() -> None:
    simple_expr = "4 - 2;"
    token_left    = Token(TokenType.NUMBER, "4", float(4), 1, 2)
    token_op      = Token(TokenType.MINUS, "-", None, 1, 4)
    token_right   = Token(TokenType.NUMBER, "2", float(2), 1, 6)
    exp_output    = [ExprStmt(BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right)))]

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output


def test_simple_mul() -> None:
    simple_expr = "4 * 4;"
    token_left    = Token(TokenType.NUMBER, "4", float(4), 1, 2)
    token_op      = Token(TokenType.STAR, "*", None, 1, 4)
    token_right   = Token(TokenType.NUMBER, "4", float(4), 1, 6)
    exp_output    = [ExprStmt(BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right)))]

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output


def test_simple_div() -> None:
    simple_expr = "6 / 4;"
    token_left    = Token(TokenType.NUMBER, "6", float(6), 1, 2)
    token_op      = Token(TokenType.SLASH, "/", None, 1, 4)
    token_right   = Token(TokenType.NUMBER, "4", float(4), 1, 6)
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


def test_parse_fib_for() -> None:
    source = load_source(FIB_FOR_PROGRAM)
    parsed_output = parse_input(source)

    exp_types = [VarStmt, VarStmt, BlockStmt]
    assert len(parsed_output) == len(exp_types)

    for p, t in zip(parsed_output, exp_types):
        assert type(p) == t


def test_parse_fib_func() -> None:
    source = load_source(FIB_FUNC_PROGRAM)
    parsed_output = parse_input(source)

    exp_types = [FuncStmt, BlockStmt]
    assert len(parsed_output) == len(exp_types)

    for p, t in zip(parsed_output, exp_types):
        assert type(p) == t


def test_parse_func() -> None:
    source = load_source(FUNC_PROGRAM)
    parsed_output = parse_input(source)

    # For loops with an initializer will be parsed into a single block statement.
    # The second for loop will be parsed into a WhileStmt
    exp_types = [FuncStmt, PrintStmt, ExprStmt]
    assert len(parsed_output) == len(exp_types)
    
    for p, t in zip(parsed_output, exp_types):
        assert type(p) == t

    # Ensure the final ExprStmt contains a CallExpr
    assert isinstance(parsed_output[2].expr, CallExpr)


def test_parse_class_fields() -> None:
    source = load_source(CLASS_FIELDS_PROGRAM)
    parsed_output = parse_input(source)
    
    exp_types = [ClassStmt, ExprStmt, ExprStmt, ExprStmt, PrintStmt, PrintStmt]

    assert len(parsed_output) == len(exp_types)
    for p, t in zip(parsed_output, exp_types):
        assert type(p) == t

    # Ensure the expression statements contain SetExprs
    assert isinstance(parsed_output[1].expr, AssignmentExpr)
    assert isinstance(parsed_output[2].expr, SetExpr)
    assert isinstance(parsed_output[3].expr, SetExpr)

    # Ensure the print statements contain GetExprs
    assert isinstance(parsed_output[4].expr, GetExpr)
    assert isinstance(parsed_output[5].expr, GetExpr)


def test_parse_class_this() -> None:
    source = load_source(CLASS_THIS_PROGRAM)
    parsed_output = parse_input(source)
    
    exp_types = [ClassStmt, ExprStmt, FuncStmt];

    assert len(parsed_output) == len(exp_types)
