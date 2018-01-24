"""
LOX Base Class

Stefan Wong 2018
"""

import sys
from loxpy import Scanner

# Debug
#from pudb import set_trace; set_trace()

class Lox(object):
    """
    Lox interpreter object.
    """
    def __init__(self):
        self.scanner = None         # Create a new scanner object when we call run
        self.token_list = []

    def _run(self, source):
        self.scanner = Scanner.Scanner(source)
        self.token_list = self.scanner.scan()

        # Dump tokens to console
        for t in self.token_list:
            print(t)

        sys.exit(1)

    def runFile(self, filename):
        with open(filename, 'r') as fp:
            source = fp.read()
        self._run(str(source))

    def runPrompt(self):
        print('TODO: not yet implemented')
