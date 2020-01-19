"""
Abstract class Expression
Generated automatically at  2:55PM NZDT on Jan 28 2018
"""

import os
import sys
from typing import Any
from typing import Type
from loxpy import Token


class Expression:
    def __init__(self) -> None:
        # NOTE : I am just doing this to cheat with mypy,
        # because these members were previously only in the
        # derived classes
        self.left  :Any = None
        self.op    :Any = None
        self.right :Any = None
        self.value :Any = None

    # TODO : type hint for function is Callable[[],]
    def accept(self, visitor) -> None:
        raise NotImplementedError("This method should be called on dervied classes")


class Binary(Expression):
    def __init__(self, left:Type[Expression], op:Token.Token, right:Type[Expression]) -> None:
        if type(op) is not Token.Token:
            raise ValueError("op must be a token")
        self.left  :Type[Expression] = left
        self.op    :Token.Token      = op
        self.right :Type[Expression] = right

    def __str__(self) -> str:
        s = []
        s.append("%s, %s, %s\n" % (str(self.left), str(self.op), str(self.right)))

        return "".join(s)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def accept(self, visitor) -> None:
        visitor.visit_binary_expr(self)


class Grouping(Expression):
    def __init__(self, expression) -> None:
        self.expression = expression

    def __str__(self) -> str:
        s = []
        s.append("%s\n" % (str(self.expression)))
        return "".join(s)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def accept(self, visitor) -> None:
        visitor.visit_grouping_expr(self)


class Literal(Expression):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        s = []
        s.append("%s\n" % (str(self.value)))

        return "".join(s)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def accept(self, visitor) -> None:
        visitor.visit_literal_expr(self)


class Unary(Expression):
    def __init__(self, op:Token.Token, right) -> None:
        if type(op) is not Token.Token:
            raise ValueError("op must be a token")
        self.op    = op
        self.right = right

    def __str__(self) -> str:
        s = []
        s.append("%s, %s\n" % (str(self.op), str(self.right)))

        return "".join(s)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def accept(self, visitor) -> None:
        visitor.visit_unary_expr(self)
