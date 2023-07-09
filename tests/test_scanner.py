"""
TEST_SCANNER
Unit tests for Scanner module

"""

from loxpy.scanner import Scanner
from loxpy.token import Token, TokenType



OPERATOR_SRC  = 'programs/op.lox'
SIMPLE_OP_SRC = 'programs/op_simple.lox'
BANG_SRC      = 'programs/op_bang.lox'

VERBOSE = False   # Turn this on to make test print more output


def load_source(filename:str) -> str:
    with open(filename, 'r') as fp:
        source = fp.read()
    return str(source)


def test_operator() -> None:
    scanner = Scanner(load_source(SIMPLE_OP_SRC), verbose=VERBOSE)
    token_list = scanner.scan()

    exp_tokens = [
        Token(TokenType.VAR       , '' , None, 1),
        Token(TokenType.IDENTIFIER, '' , None, 1),
        Token(TokenType.EQUAL,      '' , None, 1),
        Token(TokenType.NUMBER,     '2', 2.0,  1),
        Token(TokenType.PLUS,       '' , None, 1),
        Token(TokenType.NUMBER,     '2', 2.0,  1),
        Token(TokenType.SEMICOLON,  '' , None, 1),
        Token(TokenType.LOX_EOF,    '' , None, 2),
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
        Token(TokenType.VAR       , '' , None, 1),
        Token(TokenType.IDENTIFIER, '' , None, 1),
        Token(TokenType.EQUAL,      '' , None, 1),
        Token(TokenType.TRUE,       '' , None, 1),

        Token(TokenType.IDENTIFIER, '' , None, 2),
        Token(TokenType.EQUAL,      '' , None, 2),
        Token(TokenType.BANG,       '' , None, 2),
        Token(TokenType.IDENTIFIER, '' , None, 2),
        Token(TokenType.LOX_EOF,    '' , None, 3),
    ]

    #print("[%s] Output token list:" % self.bang_src)
    #for n, t in enumerate(token_list):
    #    print('%d : %s' % (n, str(t)))

    assert len(exp_tokens)== len(token_list)

    for n, (tok, exp_tok) in enumerate(zip(token_list, exp_tokens)):
        if VERBOSE and tok != exp_tok:
            print(f"Token [{n}], expected {exp_tok}, got {tok}")
        assert tok == exp_tok

