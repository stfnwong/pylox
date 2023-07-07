"""
Abstract class Expression
Generated automatically at  5:22PM BST on Jul 07 2023
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from loxpy import Token


class Expression(object):
    def accept(self, visitor):
        raise NotImplementedError("This method should be called on dervied classes")


class Binary(Expression):
    def __init__(self, left, op, right):
        if type(op) is not Token.Token:
            raise ValueError("op must be a token")
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        s = []
        s.append("%s, %s, %s\n" % (str(self.left), str(self.op), str(self.right)))

        return "".join(s)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def accept(self, visitor):
        visitor.visit_binary_expr(self)


class Grouping(Expression):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        s = []
        s.append("%s\n" % (str(self.expression)))

        return "".join(s)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def accept(self, visitor):
        visitor.visit_grouping_expr(self)


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        s = []
        s.append("%s\n" % (str(self.value)))

        return "".join(s)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def accept(self, visitor):
        visitor.visit_literal_expr(self)


class Unary(Expression):
    def __init__(self, op, right):
        if type(op) is not Token.Token:
            raise ValueError("op must be a token")
        self.op = op
        self.right = right

    def __str__(self):
        s = []
        s.append("%s, %s\n" % (str(self.op), str(self.right)))

        return "".join(s)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def accept(self, visitor):
        visitor.visit_unary_expr(self)


