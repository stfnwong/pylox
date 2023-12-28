# STATEMENTS 

from abc import ABC, abstractmethod
from dataclasses import dataclass

from loxpy.expr import Expr



@dataclass
class Stmt(ABC):

    @abstractmethod
    def accept(self, visitor):
        raise NotImplementedError("This method must be defined in derived class")


@dataclass
class ExprStmt(Stmt):
    expr: Expr

    def accept(self, visitor):
        return visitor.visit_expr_stmt(self)


@dataclass
class PrintStmt(Stmt):
    expr: Expr

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)
