"""
Abstract class Expr

"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Self, Union

from loxpy.Token import Token



@dataclass
class Expr(ABC):
    # TODO: what is the type of the visitor?
    @abstractmethod
    def accept(self, visitor) -> Self:
        pass


@dataclass
class BinaryExpr(Expr):
    op: Token
    left: Expr
    right: Expr

    def accept(self, visitor) -> Optional[float]:
        return visitor.visit_binary_expr(self)


@dataclass
class GroupingExpr(Expr):
    expression: Expr

    def accept(self, visitor) -> Expr:
        return visitor.visit_grouping_expr(self)


@dataclass
class LiteralExpr(Expr):
    value: Token

    def accept(self, visitor) -> Expr:
        return visitor.visit_literal_expr(self)


@dataclass
class UnaryExpr(Expr):
    right: Expr
    op: Token

    # TODO: can this return an expression?
    def accept(self, visitor) -> Union[float, bool, None]:
        return visitor.visit_unary_expr(self)
