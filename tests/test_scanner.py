"""
TEST_SCANNER
Unit tests for Scanner module

Stefan Wong 2018
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
# module under test
from loxpy import Scanner
from loxpy import Token

# Debug
#from pudb import set_trace; set_trace()

def load_source(filename):
    with open(filename, 'r') as fp:
        source = fp.read()
    return str(source)

class TestScanner(unittest.TestCase):
    def setUp(self):
        self.operator_src = 'lox_src/op.lox'
        self.simple_op_src = 'lox_src/op_simple.lox'
        self.verbose = True

    def test_operator(self):
        src = load_source(self.simple_op_src)
        scanner = Scanner.Scanner(src, verbose=self.verbose)
        token_list = scanner.scan()

        if self.verbose:
            print("Output token list:")
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

        for n, t in enumerate(token_list):
            if t != exp_tokens[n]:
                print("Token %d mismatch" % n)
                print("output   : %s " % t)
                print("expected : %s " % exp_tokens[n])
                self.assertEqual(t, exp_tokens[n])      # cause test to fail


if __name__ == '__main__':
    unittest.main()
