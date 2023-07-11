"""
Abstract class Expr

"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Self, Union

from loxpy.token import Token



@dataclass
class Expr(ABC):
    # TODO: what is the type of the visitor?
    @abstractmethod
    def accept(self, visitor) -> Self:
        pass


# All derived classes have a custom __str__() method to make the ASTPrinter work

@dataclass
class BinaryExpr(Expr):
    op: Token
    left: Expr
    right: Expr

    def __str__(self) -> str:
        return f"BinaryExpr({self.op.lexeme}, {self.left}, {self.right})"

    def accept(self, visitor) -> Optional[float]:
        return visitor.visit_binary_expr(self)


@dataclass
class GroupingExpr(Expr):
    expression: Expr

    def __str__(self) -> str:
        return f"GroupingExpr({self.expression})"

    def accept(self, visitor) -> Expr:
        return visitor.visit_grouping_expr(self)


@dataclass
class LiteralExpr(Expr):
    value: Token

    def __str__(self) -> str:
        return f"LiteralExpr({self.value})"

    def accept(self, visitor) -> Expr:
        return visitor.visit_literal_expr(self)


@dataclass
class UnaryExpr(Expr):
    op: Token
    right: Expr

    def __str__(self) -> str:
        return f"UnaryExpr({self.op}, {self.right})"

    # TODO: can this return an expression?
    def accept(self, visitor) -> Union[float, bool, None]:
        return visitor.visit_unary_expr(self)
