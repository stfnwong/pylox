"""
TEST_PARSER
Unit tests for lox parser

Stefan Wong 2018
"""

import os
import sys
import unittest
# Modules under test
from loxpy import Parser
from loxpy import Scanner
from loxpy import Expression
from loxpy import Token

# Debug
#from pudb import set_trace; set_trace()


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.verbose = True

    def test_simple_expr(self) -> None:
        # Input expression
        simple_expr = '2 + 2;'

        # Format the expected output
        token_left    = Token.Token(Token.NUMBER, '2', float(2), 1)
        token_op      = Token.Token(Token.PLUS, '', None, 1)
        token_right   = Token.Token(Token.NUMBER, '2', float(2), 1)
        exp_output  = Expression.Binary(token_left, token_op, token_right)

        scanner    = Scanner.Scanner(simple_expr)
        token_list = scanner.scan()
        parser     = Parser.Parser(token_list)

        # Show in console what the parsed output was
        print(parser)
        parsed_output = parser.parse()
        print(type(parsed_output))
        print(parsed_output)

        exp_left  = Expression.Literal(token_left)
        exp_right = Expression.Literal(token_right)

        # Now check that the output matches
        self.assertEqual(exp_left, parsed_output.left)
        self.assertEqual(exp_right, parsed_output.right)
        self.assertEqual(token_op, parsed_output.op)



if __name__ == '__main__':
    unittest.main()

