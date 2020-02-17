"""
TEST_INTERPRETER

Stefan Wong 2018
"""

import os
import sys
import unittest
# modules under test
from loxpy import Interpreter
from loxpy import Parser
from loxpy import Scanner
from loxpy import Expression
from loxpy import Token

# debug
from pudb import set_trace; set_trace()


def load_source(filename:str) -> str:
    with open(filename, 'r') as fp:
        source = fp.read()
    return str(source)


class TestInterpreter(unittest.TestCase):
    def setUp(self) -> None:
        self.verbose:bool = True

    def test_interpret_bang(self) -> None:
        pass

    def test_interpret_unary(self) -> None:
        # Get an interpreter
        interp = Interpreter.Interpreter(verbose = self.verbose)
        # Create test expression
        tok_bang = Token.Token(Token.BANG, "!", None, 1)
        tok_iden = Token.Token(Token.IDENTIFIER, "a", None, 1)
        expr     = Expression.Unary(tok_bang, tok_iden)
        print('Interpreting expression [%s]' % str(expr))

        # interpret the expression
        value = interp.interpret(expr)
        print(value)
        self.assertIsNotNone(value)

    def test_interpret_unary_from_source(self) -> None:
        unary_file = 'loxsrc/unary.lox'
        unary_source = load_source(unary_file)

        # Parse the source
        scanner = Scanner.Scanner(unary_source)
        unary_tokens = scanner.scan()
        parser = Parser.Parser(unary_tokens)
        unary_expr = parser.parse()

    def test_interpret_binary(self) -> None:
        interp = Interpreter.Interpreter(verbose = self.verbose)
        tok_num1 = Token.Token(Token.NUMBER, "2", None, 1)
        tok_mul  = Token.Token(Token.STAR, "*", None, 1)
        tok_num2 = Token.Token(Token.NUMBER, "4", None, 1)

        expr     = Expression.Binary(tok_num1, tok_mul, tok_num2)
        print('Interpreting expression [%s]' % str(expr))

        # interpret the expression
        value = interp.interpret(expr)
        print(value)
        self.assertIsNotNone(value)

if __name__ == "__main__":
    unittest.main()
