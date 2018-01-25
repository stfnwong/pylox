"""
PARSER

Stefan Wong 2018
"""

from loxpy import Expression
from loxpy import Token

class Parser(object):
    def __init__(self, token_list):
        if type(token_list) is not list:
            raise ValueError('token_list must be a list')
        self.token_list = token_list
        self.current = 0

    # Methods for seeking through the token list
    def _at_end(self):
        cur_token = self._peek()
        if cur_token.token_type == Token.LOX_EOF:
            return True
        return False

    def _peek(self):
        return self.token_list[self.current]

    def _previous(self):
        return self.token_list[self.current - 1]

    # Methods that implement rules for productions
    def _match(self):
        pass

    def _equality(self):
        pass



    # Expand an expression
    def expression(self):
        pass
