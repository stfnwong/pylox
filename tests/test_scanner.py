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


def load_source(filename):
    with open(filename, 'r') as fp:
        source = fp.read()

    return str(source)

class TestScanner(unittest.TestCase):
    def setUp(self):
        self.operator_src = 'lox_src/op.lox'

    def test_operator(self):
        src = load_source(self.operator_src)
        scanner = Scanner.Scanner(src)
        token_list = scanner.scan()

        for t in token_list:
            print(t)


if __name__ == '__main__':
    unittest.main()
