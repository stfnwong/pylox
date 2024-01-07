"""
TEST_SCANNER
Unit tests for Scanner module

"""

from loxpy.scanner import Scanner
from loxpy.token import Token, TokenType
from loxpy.util import load_source


OPERATOR_SRC  = 'programs/op.lox'
SIMPLE_OP_SRC = 'programs/op_simple.lox'
BANG_SRC      = 'programs/op_bang.lox'
FOR_SRC      = 'programs/for_interp.lox'

VERBOSE = False   # Turn this on to make test print more output



def test_operator() -> None:
    scanner = Scanner(load_source(SIMPLE_OP_SRC), verbose=VERBOSE)
    token_list = scanner.scan()

    exp_tokens = [
        Token(TokenType.VAR       , "var", "var", 1, 4),
        Token(TokenType.IDENTIFIER, "c",   "c",   1, 6),
        Token(TokenType.EQUAL,      "=",   None,  1, 8),
        Token(TokenType.NUMBER,     "2",   2.0,   1, 10),
        Token(TokenType.PLUS,       "+",   None,  1, 12),
        Token(TokenType.NUMBER,     '2',   2.0,   1, 14),
        Token(TokenType.SEMICOLON,  ";",   None,  1, 15),
        Token(TokenType.LOX_EOF,    "",    None,  2, 0),
    ]

    assert len(exp_tokens) == len(token_list)

    for n, (tok, exp_tok) in enumerate(zip(token_list, exp_tokens)):
        if VERBOSE and tok != exp_tok:
            print(f"Token [{n}], expected {exp_tok}, got {tok}")
        assert tok == exp_tok


def test_bang() -> None:
    scanner = Scanner(load_source(BANG_SRC), verbose=VERBOSE)
    token_list = scanner.scan()

    exp_tokens = [
        Token(TokenType.VAR       , "var",  "var",  1, 4),
        Token(TokenType.IDENTIFIER, "a" ,   "a",    1, 6),
        Token(TokenType.EQUAL,      "=" ,   None,   1, 8),
        Token(TokenType.TRUE,       "true", "true", 1, 13),
        Token(TokenType.SEMICOLON,  ";",    None,   1, 14),

        Token(TokenType.IDENTIFIER, "a",    "a",    2, 2),
        Token(TokenType.EQUAL,      "=",    None,   2, 4),
        Token(TokenType.BANG,       "!",    None,   2, 6),
        Token(TokenType.IDENTIFIER, "a",    "a",    2, 7),
        Token(TokenType.SEMICOLON,  ";",    None,   2, 8),
        Token(TokenType.LOX_EOF,    "" ,    None,   3, 0),
    ]

    assert len(exp_tokens)== len(token_list)

    for n, (tok, exp_tok) in enumerate(zip(token_list, exp_tokens)):
        if VERBOSE and tok != exp_tok:
            print(f"Token [{n}], expected {exp_tok}, got {tok}")
        assert tok == exp_tok



def test_for() -> None:
    scanner = Scanner(load_source(FOR_SRC), verbose=VERBOSE)
    token_list = scanner.scan()

    exp_tokens = [
        Token(TokenType.VAR       , "var",    "var",   5, 4),
        Token(TokenType.IDENTIFIER, "i" ,     "i",     5, 6),
        Token(TokenType.SEMICOLON,  ";",      None,    5, 7),

        Token(TokenType.FOR,         "for" ,  "for",   6, 4),
        Token(TokenType.LEFT_PAREN,  "(" ,    None,    6, 5),
        Token(TokenType.IDENTIFIER,  "i" ,    "i",     6, 6),
        Token(TokenType.EQUAL,       "=" ,    None,    6, 8),
        Token(TokenType.NUMBER,      "0" ,    0.0,     6, 10),
        Token(TokenType.SEMICOLON,   ";",     None,    6, 11),
        Token(TokenType.IDENTIFIER,  "i" ,    "i",     6, 13),
        Token(TokenType.LESS,        "<" ,    None,    6, 15),
        Token(TokenType.NUMBER,      "10" ,   10.0,    6, 18),
        Token(TokenType.SEMICOLON,   ";",     None,    6, 19),
        Token(TokenType.IDENTIFIER,  "i" ,    "i",     6, 21),
        Token(TokenType.EQUAL,       "=" ,    None,    6, 23),
        Token(TokenType.IDENTIFIER,  "i" ,    "i",     6, 25),
        Token(TokenType.PLUS,        "+" ,    None,    6, 27),
        Token(TokenType.NUMBER,      "1" ,    1.0,     6, 29),
        Token(TokenType.RIGHT_PAREN, ")" ,    None,    6, 30),

        Token(TokenType.LEFT_BRACE,  "{" ,    None,    6, 32),

        Token(TokenType.PRINT,       "print", "print", 7, 7),
        Token(TokenType.LEFT_PAREN,  "(" ,    None,    7, 8),
        Token(TokenType.IDENTIFIER,  "i" ,    "i",     7, 9),
        Token(TokenType.RIGHT_PAREN,  ")" ,   None,    7, 10),
        Token(TokenType.SEMICOLON,   ";",     None,    7, 11),

        Token(TokenType.RIGHT_BRACE,  "}" ,   None,    8, 2),
        Token(TokenType.LOX_EOF,    "",       None,    9, 0),
    ]

    assert len(token_list) == len(exp_tokens)

    for n, (tok, exp_tok) in enumerate(zip(token_list, exp_tokens)):
        if VERBOSE and tok != exp_tok:
            print(f"Token [{n}], expected {exp_tok}, got {tok}")
        assert tok == exp_tok
