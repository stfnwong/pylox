"""
TEST_AST_PRINT

Stefan Wong 2018
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
# modules under test
from tools import ASTPrint
from loxpy import Token
from loxpy import Expression

# Debug
#from pudb import set_trace; set_trace()

class TestASTPrint(unittest.TestCase):
    def setUp(self):
        self.verbose = True
        self.test_expr = '2 + 2;'

    def test_parenthesize(self):

        left      = Token.Token(Token.NUMBER, '2', 2.0, 1)
        op        = Token.Token(Token.PLUS, '', None, 1)
        right     = Token.Token(Token.NUMBER, '4', 4.0, 1)
        test_expr = Expression.Binary(left, op, right)
        expr_list = [test_expr]
        ast_print = ASTPrint.ASTPrint()
        ast_string = ast_print.ast_print(test_expr)
        #ast_string = ast_print._parenthesize('expr', expr_list)

        print(ast_string)



if __name__ == '__main__':
    unittest.main()
