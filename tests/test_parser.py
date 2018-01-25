"""
TEST_PARSER
Unit tests for lox parser

Stefan Wong 2018
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
# Modules under test
from loxpy import Parser
from loxpy import Scanner

# Debug
#from pudb import set_trace; set_trace()

class TestParser(unittest.TestCase):
    def setUp(self):
        self.verbose = True
        self.simple_expr = '2 + 2;'

    def test_simple_expr(self):
        scanner = Scanner.Scanner(self.simple_expr)
        token_list = scanner.scan()
        parser = Parser.Parser(token_list)

        # TODO : actually exmine the parsed output
        print(parser)
        parsed_output = parser.parse()
        print(type(parsed_output))
        print(parsed_output)

if __name__ == '__main__':
    unittest.main()

