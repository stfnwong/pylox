# Modules under test
from loxpy import Parser, Scanner, Token
from loxpy.Expression import BinaryExpr, LiteralExpr


def test_simple_add() -> None:
    # Input expression
    simple_expr = '2 + 2;'
    # Format the expected output
    token_left    = Token.Token(Token.NUMBER, '2', float(2), 1)
    token_op      = Token.Token(Token.PLUS, '', None, 1)
    token_right   = Token.Token(Token.NUMBER, '2', float(2), 1)
    exp_output    = BinaryExpr(token_op, token_left, token_right)

    # Get some objects to test
    scanner       = Scanner.Scanner(simple_expr)
    token_list    = scanner.scan()
    parser        = Parser.Parser(token_list)
    parsed_output = parser.parse()

    # Now check that the output matches
    exp_left  = LiteralExpr(token_left)
    exp_right = LiteralExpr(token_right)
    assert exp_left == parsed_output.left
    assert exp_right == parsed_output.right
    assert token_op == parsed_output.op

def test_simple_sub() -> None:
    simple_expr = '4 - 2;'
    # Format the expected output
    token_left    = Token.Token(Token.NUMBER, '4', float(4), 1)
    token_op      = Token.Token(Token.MINUS, '', None, 1)
    token_right   = Token.Token(Token.NUMBER, '2', float(2), 1)
    exp_output    = BinaryExpr(token_op, token_left, token_right)

    # Get some objects to test
    scanner       = Scanner.Scanner(simple_expr)
    token_list    = scanner.scan()
    parser        = Parser.Parser(token_list)
    parsed_output = parser.parse()

    # Now check that the output matches
    exp_left  = LiteralExpr(token_left)
    exp_right = LiteralExpr(token_right)
    assert exp_left == parsed_output.left
    assert exp_right == parsed_output.right
    assert token_op == parsed_output.op

def test_simple_mul() -> None:
    simple_expr = '4 * 4;'
    # Format the expected output
    token_left    = Token.Token(Token.NUMBER, '4', float(4), 1)
    token_op      = Token.Token(Token.STAR, '', None, 1)
    token_right   = Token.Token(Token.NUMBER, '4', float(4), 1)
    exp_output    = BinaryExpr(token_op, token_left, token_right)
    print(f"exp_output: {exp_output}")

    # Get some objects to test
    scanner       = Scanner.Scanner(simple_expr)
    token_list    = scanner.scan()
    parser        = Parser.Parser(token_list)
    parsed_output = parser.parse()

    assert parsed_output.left == LiteralExpr(token_left)
    assert parsed_output.right == LiteralExpr(token_right)
    assert parsed_output.op == token_op

def test_simple_div() -> None:
    simple_expr = '6 / 4;'
    # Format the expected output
    token_left    = Token.Token(Token.NUMBER, '6', float(6), 1)
    token_op      = Token.Token(Token.SLASH, '', None, 1)
    token_right   = Token.Token(Token.NUMBER, '4', float(4), 1)
    exp_output    = BinaryExpr(token_op, token_left, token_right)
    print(f"exp_output: {exp_output}")

    # Get some objects to test
    scanner       = Scanner.Scanner(simple_expr)
    token_list    = scanner.scan()
    parser        = Parser.Parser(token_list)
    parsed_output = parser.parse()

    assert parsed_output.left == LiteralExpr(token_left)
    assert parsed_output.right == LiteralExpr(token_right)
    assert parsed_output.op == token_op
