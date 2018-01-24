"""
EXPRESSION

Stefan Wong 2018
"""

from loxpy import Token

# For now, I won't bother to make this explicitly abstract
class Expression(object):
    pass

class BinaryExpression(Expression):
    def __init__(self, left, op, right):
        if type(op) is not Token.Token:
            raise ValueError('op must be a token')
        self.left = left
        self.op = op        # enforce token?
        self.right = right

    def __str__(self):
        s = []
        s.append('%s %s %s' % (self.left, Token.TOKEN_SYMBOL[self.op], self.right))

        return ''.join(s)

    def __repr__(self):
        return self.__str__()
