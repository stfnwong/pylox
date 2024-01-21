from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, Sequence, Union

from loxpy.token import Token


ResultType = Union[float, bool, str, None]


@dataclass(frozen=True)
class Expr(ABC):
    # TODO: what is the type of the visitor?
    @abstractmethod
    def accept(self, visitor) -> Any:
        raise NotImplemented


# All derived classes have a custom __str__() method to make the ASTPrinter work


@dataclass(frozen=True)
class BinaryExpr(Expr):
    op: Token
    left: Expr
    right: Expr

    def __str__(self) -> str:
        return f"BinaryExpr({self.op.lexeme}, {self.left}, {self.right})"

    def accept(self, visitor) -> Optional[float]:
        return visitor.visit_binary_expr(self)


@dataclass(frozen=True)
class CallExpr(Expr):
    callee: Expr
    paren: Token
    arguments: Sequence[Expr]

    def __str__(self) -> str:
        return f"CallExpr({self.arguments})"

    def accept(self, visitor) -> Any:
        return visitor.visit_call_expr(self)



@dataclass(frozen=True)
class GetExpr(Expr):
    obj: Expr
    name: Token

    def __str__(self) -> str:
        return f"GetExpr({self.name}: {self.obj})"

    def accept(self, visitor) -> Expr:
        return visitor.visit_get_expr(self)


@dataclass(frozen=True)
class SetExpr(Expr):
    obj: Expr
    name: Token
    value: Expr

    def __str__(self) -> str:
        return f"SetExpr({self.name}: {self.obj}) -> {self.value}"

    def accept(self, visitor) -> Expr:
        return visitor.visit_set_expr(self)


@dataclass(frozen=True)
class SuperExpr(Expr):
    keyword: Token
    method: Token

    def __str__(self) -> str:
        return f"SuperExpr({self.keyword})"

    def accept(self, visitor) -> Expr:
        return visitor.visit_super_expr(self)


@dataclass(frozen=True)
class ThisExpr(Expr):
    keyword: Token

    def __str__(self) -> str:
        return f"ThisExpr({self.keyword})"

    def accept(self, visitor) -> Expr:
        return visitor.visit_this_expr(self)


@dataclass(frozen=True)
class GroupingExpr(Expr):
    expression: Expr

    def __str__(self) -> str:
        return f"GroupingExpr({self.expression})"

    def accept(self, visitor) -> Expr:
        return visitor.visit_grouping_expr(self)


@dataclass(frozen=True)
class LiteralExpr(Expr):
    value: Token

    def __str__(self) -> str:
        return f"LiteralExpr({self.value})"

    def accept(self, visitor) -> Expr:
        return visitor.visit_literal_expr(self)


@dataclass(frozen=True)
class LogicalExpr(Expr):
    op: Token
    left: Expr
    right: Expr

    def __str__(self) -> str:
        return f"LogicalExpr({self.op}, {self.left}, {self.right})"

    def accept(self, visitor) -> Expr:
        return visitor.visit_logical_expr(self)


@dataclass(frozen=True)
class UnaryExpr(Expr):
    op: Token
    right: Expr

    def __str__(self) -> str:
        return f"UnaryExpr({self.op}, {self.right})"

    def accept(self, visitor) -> Union[Expr, float, bool, None]:
        return visitor.visit_unary_expr(self)


@dataclass(frozen=True)
class VarExpr(Expr):
    name: Token

    def __str__(self) -> str:
        return f"VarExpr({self.name.lexeme})"

    def accept(self, visitor) -> Any:
        return visitor.visit_var_expr(self)


@dataclass(frozen=True)
class AssignmentExpr(Expr):
    name: Token
    value: Expr

    def __str__(self) -> str:
        return f"AssignmentExpr({self.name})"

    def accept(self, visitor) -> Any:
        return visitor.visit_assignment_expr(self)
