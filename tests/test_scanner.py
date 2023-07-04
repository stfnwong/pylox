"""
TEST_SCANNER
Unit tests for Scanner module

Stefan Wong 2018
"""

import os
import sys
import unittest
# module under test
from loxpy import Scanner
from loxpy import Token

# Debug
#from pudb import set_trace; set_trace()

def load_source(filename:str) -> str:
    with open(filename, 'r') as fp:
        source = fp.read()
    return str(source)


class TestScanner(unittest.TestCase):
    def setUp(self) -> None:
        self.operator_src  = 'programs/op.lox'
        self.simple_op_src = 'programs/op_simple.lox'
        self.bang_src      = 'programs/op_bang.lox'
        self.verbose       = True

    def test_operator(self) -> None:
        src = load_source(self.simple_op_src)
        scanner = Scanner.Scanner(src, verbose=self.verbose)
        token_list = scanner.scan()

        print("[%s] Output token list:" % self.simple_op_src)
        for n, t in enumerate(token_list):
            print('%d : %s' % (n, str(t)))

        exp_tokens = []     # expected output
        exp_tokens.append(Token.Token(Token.VAR       , '' , None, 1))
        exp_tokens.append(Token.Token(Token.IDENTIFIER, '' , None, 1))
        exp_tokens.append(Token.Token(Token.EQUAL,      '' , None, 1))
        exp_tokens.append(Token.Token(Token.NUMBER,     '2', 2.0,  1))
        exp_tokens.append(Token.Token(Token.PLUS,       '' , None, 1))
        exp_tokens.append(Token.Token(Token.NUMBER,     '2', 2.0,  1))
        exp_tokens.append(Token.Token(Token.SEMICOLON,  '' , None, 1))
        exp_tokens.append(Token.Token(Token.LOX_EOF,    '' , None, 2))

        self.assertEqual(len(exp_tokens), len(token_list))

        for n, t in enumerate(token_list):
            if t != exp_tokens[n]:
                print("Token %d mismatch" % n)
                print("output   : %s " % t)
                print("expected : %s " % exp_tokens[n])
            self.assertEqual(t, exp_tokens[n])

    def test_bang(self) -> None:
        src = load_source(self.bang_src)
        scanner = Scanner.Scanner(src, verbose=self.verbose)
        token_list = scanner.scan()

        exp_tokens = []
        exp_tokens.append(Token.Token(Token.VAR       , '' , None, 1))
        exp_tokens.append(Token.Token(Token.IDENTIFIER, '' , None, 1))
        exp_tokens.append(Token.Token(Token.EQUAL,      '' , None, 1))
        exp_tokens.append(Token.Token(Token.TRUE,       '' , None, 1))

        exp_tokens.append(Token.Token(Token.IDENTIFIER, '' , None, 2))
        exp_tokens.append(Token.Token(Token.EQUAL,      '' , None, 2))
        exp_tokens.append(Token.Token(Token.BANG,       '' , None, 2))
        exp_tokens.append(Token.Token(Token.IDENTIFIER, '' , None, 2))
        exp_tokens.append(Token.Token(Token.LOX_EOF,    '' , None, 3))

        print("[%s] Output token list:" % self.bang_src)
        for n, t in enumerate(token_list):
            print('%d : %s' % (n, str(t)))

        self.assertEqual(len(exp_tokens), len(token_list))

        for n, t in enumerate(token_list):
            if t != exp_tokens[n]:
                print("Token %d mismatch" % n)
                print("output   : %s " % t)
                print("expected : %s " % exp_tokens[n])
            self.assertEqual(t, exp_tokens[n])


if __name__ == '__main__':
    unittest.main()
