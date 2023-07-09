# Modules under test
from loxpy import Parser, Scanner, Token
from loxpy.Expression import Expr, BinaryExpr, LiteralExpr



def parse_input(expr_src: str) -> Expr:
    scanner       = Scanner.Scanner(expr_src)
    token_list    = scanner.scan()
    parser        = Parser.Parser(token_list)
    parsed_output = parser.parse()

    return parsed_output


def test_simple_add() -> None:
    simple_expr = '2 + 2;'
    # Format the expected output
    token_left    = Token.Token(Token.NUMBER, '2', float(2), 1)
    token_op      = Token.Token(Token.PLUS, '', None, 1)
    token_right   = Token.Token(Token.NUMBER, '2', float(2), 1)
    exp_output    = BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right))

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output

def test_simple_sub() -> None:
    simple_expr = '4 - 2;'
    # Format the expected output
    token_left    = Token.Token(Token.NUMBER, '4', float(4), 1)
    token_op      = Token.Token(Token.MINUS, '', None, 1)
    token_right   = Token.Token(Token.NUMBER, '2', float(2), 1)
    exp_output    = BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right))

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output

def test_simple_mul() -> None:
    simple_expr = '4 * 4;'
    # Format the expected output
    token_left    = Token.Token(Token.NUMBER, '4', float(4), 1)
    token_op      = Token.Token(Token.STAR, '', None, 1)
    token_right   = Token.Token(Token.NUMBER, '4', float(4), 1)
    exp_output    = BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right))

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output

def test_simple_div() -> None:
    simple_expr = '6 / 4;'
    # Format the expected output
    token_left    = Token.Token(Token.NUMBER, '6', float(6), 1)
    token_op      = Token.Token(Token.SLASH, '', None, 1)
    token_right   = Token.Token(Token.NUMBER, '4', float(4), 1)
    exp_output    = BinaryExpr(token_op, LiteralExpr(token_left), LiteralExpr(token_right))

    parsed_output = parse_input(simple_expr)

    assert parsed_output == exp_output
