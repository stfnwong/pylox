from typing import Sequence

from loxpy.expr import BinaryExpr, LiteralExpr, UnaryExpr
from loxpy.statement import Stmt, ExprStmt, PrintStmt
from loxpy.token import Token, TokenType
from loxpy.scanner import Scanner
from loxpy.parser import Parser
from loxpy.interpreter import Interpreter
from loxpy.resolver import Resolver
from loxpy.callable import LoxClass, LoxInstance
from loxpy.util import load_source, float_equal


GLOBAL_VERBOSE = False

WHILE_PROGRAM = "programs/while.lox"
FOR_PROGRAM = "programs/for_interp.lox"


def parse_input(expr_src: str) -> Sequence[Stmt]:
    scanner       = Scanner(expr_src)
    token_list    = scanner.scan()
    parser        = Parser(token_list)
    parsed_output = parser.parse()

    return parsed_output



def test_interpret_unary() -> None:
    interp = Interpreter(verbose=GLOBAL_VERBOSE)
    resolver = Resolver(interp)

    # Test unary on number types
    operand = Token(TokenType.NUMBER, "2", None, 1)
    tok_minus  = Token(TokenType.MINUS, "-", None, 1)
    expr = [ExprStmt(UnaryExpr(tok_minus, LiteralExpr(operand)))]

    value = interp.interpret(expr)
    exp_value = -2.0

    assert float_equal(value[0], exp_value)

    # Test unary on boolean type 
    operand = Token(TokenType.TRUE, "true", "true", 1)
    tok_bang  = Token(TokenType.BANG, "!", None, 1)
    expr = [ExprStmt(UnaryExpr(tok_bang, LiteralExpr(operand)))]

    resolver.resolve(expr)
    value = interp.interpret(expr)   # NOTE: output is a list of values
    exp_value = False

    assert exp_value == value[0]

    # Bang works on number types, but it just applies "not is_true(v)" on any value v.
    # Since the truthiness of any value is True, this will always return False for any
    # numerical value
    operand = Token(TokenType.NUMBER, "2", None, 1)
    tok_bang  = Token(TokenType.BANG, "!", None, 1)
    expr = [ExprStmt(UnaryExpr(tok_bang, LiteralExpr(operand)))]

    value = interp.interpret(expr)
    exp_value = False

    assert exp_value == value[0]


def test_interpret_binary() -> None:
    interp = Interpreter(verbose=GLOBAL_VERBOSE)
    resolver = Resolver(interp)

    op_tokens = [
        Token(TokenType.PLUS, "+", None, 1),
        Token(TokenType.MINUS, "-", None, 1),
        Token(TokenType.STAR, "*", None, 1),
        Token(TokenType.SLASH, "/", None, 1)
    ]
    exp_values = [6.0, -2.0, 8.0, 0.5]

    tok_num1 = Token(TokenType.NUMBER, "2", None, 1)
    tok_num2 = Token(TokenType.NUMBER, "4", None, 1)

    
    interp_values = []
    for op_tok in op_tokens:
        expr  = [ExprStmt(BinaryExpr(op_tok, LiteralExpr(tok_num1), LiteralExpr(tok_num2)))]
        resolver.resolve(expr)
        value = interp.interpret(expr)
        interp_values.extend(value)

    for val, exp_val in zip(interp_values, exp_values):
        assert float_equal(val, exp_val)


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
    resolver = Resolver(interp)

    tok_string = Token(TokenType.STRING, "bet you can't print this", None, 1)
    stmts = [PrintStmt(LiteralExpr(tok_string))]

    resolver.resolve(stmts)
    ret = interp.interpret(stmts)
    assert len(ret) == 1
    assert ret[0] == tok_string


def test_interpret_while() -> None:
    source   = load_source(WHILE_PROGRAM)
    stmts    = parse_input(source)
    interp   = Interpreter(verbose=GLOBAL_VERBOSE)
    resolver = Resolver(interp)

    resolver.resolve(stmts)
    interp.interpret(stmts)

    expected_state = {"i": 10.0}
    for var_name in expected_state:
        assert var_name in interp.environment.values
        assert interp.environment.values[var_name] == expected_state[var_name]


# The program in this test should have the same result as the 
# program in the while test.
def test_interpret_for() -> None:
    source   = load_source(FOR_PROGRAM)
    stmts    = parse_input(source)
    interp   = Interpreter(verbose=GLOBAL_VERBOSE)
    resolver = Resolver(interp)

    resolver.resolve(stmts)
    interp.interpret(stmts)

    expected_state = {"i": 10.0}
    for var_name in expected_state:
        assert var_name in interp.environment.values
        assert interp.environment.values[var_name] == expected_state[var_name]


def test_interpret_fib_for() -> None:
    source   = load_source("programs/fib_for.lox")
    stmts    = parse_input(source)
    interp   = Interpreter(verbose=GLOBAL_VERBOSE)
    resolver = Resolver(interp)

    resolver.resolve(stmts)
    interp.interpret(stmts)

    expected_state = {"a": 1597.0, "temp": 987.0}
    for var_name in expected_state:
        assert var_name in interp.environment.values
        assert interp.environment.values[var_name] == expected_state[var_name]


def test_interpret_class_fields() -> None:
    source   = load_source("programs/class_fields.lox")
    stmts    = parse_input(source)
    interp   = Interpreter(verbose=GLOBAL_VERBOSE)
    resolver = Resolver(interp)

    resolver.resolve(stmts)
    interp.interpret(stmts)

    # NOTE: we just check the type for now to avoid having to 
    # construct a whole instance to check.
    expected_state = {
        "Test": LoxClass,
        "test": LoxInstance
    }

    for var_name, var_type in expected_state.items():
        assert var_name in interp.environment.values
        assert isinstance(interp.environment.values[var_name], var_type)

