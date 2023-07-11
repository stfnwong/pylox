"""
LOX Base Class

"""

import sys
from loxpy.scanner import Scanner


HAD_ERROR = False

# error reporting helper functions
def report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error: {where} : {message}")
    HAD_ERROR = True

def error(line, message):
    report(line, "", message)


class Lox:
    """
    Lox interpreter wrapper.
    """

    def __init__(self, verbose:bool = False):
        self.verbose = verbose
        self.scanner = None         # Create a new scanner object when we call run
        self.token_list = []

    def _run(self, source):
        self.scanner = Scanner(source)
        self.token_list = self.scanner.scan()

        # Dump tokens to console
        for t in self.token_list:
            print(t)

        sys.exit(1)

    def run_file(self, filename: str):
        with open(filename, 'r') as fp:
            source = fp.read()
        self._run(str(source))

    def run_prompt(self):
        print('TODO: not yet implemented')
