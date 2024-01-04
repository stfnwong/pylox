# STATEMENTS 

from typing import Any, List, Optional, Sequence
from abc import ABC, abstractmethod
from dataclasses import dataclass

from loxpy.expr import Expr
from loxpy.token import Token

# TODO: what should the type of the visitor be?


@dataclass
class Stmt(ABC):

    @abstractmethod
    def accept(self, visitor) -> Optional[Any]:
        raise NotImplementedError("This method must be defined in derived class")


@dataclass
class ExprStmt(Stmt):
    expr: Expr

    def accept(self, visitor):
        return visitor.visit_expr_stmt(self)


@dataclass
class FuncStmt(Stmt):
    name: Token
    params: Sequence[Token]
    body: Sequence[Stmt]

    def accept(self, visitor):
        return visitor.visit_func_stmt(self)


@dataclass
class IfStmt(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Optional[Stmt]

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)


@dataclass 
class BlockStmt(Stmt):
    stmts: List[Stmt]

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)


@dataclass
class PrintStmt(Stmt):
    expr: Expr

    def accept(self, visitor) -> Any:
        return visitor.visit_print_stmt(self)


@dataclass
class VarStmt(Stmt):
    name: Token
    initializer: Optional[Expr] = None

    def __str__(self) -> str:
        return f"VarExpr({self.name} = {self.initializer})"

    def accept(self, visitor) -> Any:
        return visitor.visit_var_stmt(self)


@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: Stmt

    def accept(self, visitor) -> Any:
        return visitor.visit_while_stmt(self)

