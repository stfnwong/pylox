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
#from pudb import set_trace; set_trace()

def load_source(filename:str) -> str:
    with open(filename, 'r') as fp:
        source = fp.read()
    return str(source)


class TestInterpreter(unittest.TestCase):
    def setUp(self) -> None:
        self.verbose = True

    def test_interpret_unary(self) -> None:
        # Create test expression
        tok_bang = Token.Token(Token.BANG, "!", None, 1)
        tok_iden = Token.Token(Token.IDENTIFIER, "a", None, 1)
        expr = Expression.Unary(tok_bang, tok_iden)
        # Get an interpreter
        interp = Interpreter.Interpreter()
        interp.interpret(expr)

    def test_interpret_unary_from_source(self):
        unary_file = 'loxsrc/unary.lox'
        unary_source = load_source(unary_file)

        # Parse the source
        scanner = Scanner.Scanner(unary_source)
        unary_tokens = scanner.scan()
        parser = Parser.Parser(unary_tokens)
        unary_expr = parser.parse()

if __name__ == "__main__":
    unittest.main()
