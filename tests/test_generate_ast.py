"""
TEST_GENERATE_AST
Test cases for AST generation

Stefan Wong 2018
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
# modules under test
from tools import GenerateAST

# Debug
#from pudb import set_trace; set_trace()


class TestGenerateAST(unittest.TestCase):
    def setUp(self):
        self.output_dir = 'tests/ast'
        self.verbose = True

    def test_generate_ast_binary(self):
        gen = GenerateAST.GenerateAST(self.output_dir, verbose=self.verbose)
        gen.main()

        print(gen)

if __name__ == '__main__':
    unittest.main()
