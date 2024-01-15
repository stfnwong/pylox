# Visitor ABC
from abc import ABC, abstractmethod
from typing import Any, Optional

from loxpy.expr import Expr
from loxpy.statement import Stmt


class Visitor(ABC):

    # ======== Expression Visitors ======== #
    @abstractmethod
    def visit_assignment_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_binary_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_call_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_get_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_grouping_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_literal_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_logical_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_set_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_super_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_this_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_unary_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_var_expr(self, expr: Expr) -> Optional[Any]:
        raise NotImplemented

    # ======== Statement Visitors ======== #
    @abstractmethod
    def visit_block_stmt(self, stmt: Stmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_class_stmt(self, stmt: Stmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_expr_stmt(self, stmt: Stmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_func_stmt(self, stmt: Stmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_if_stmt(self, stmt: Stmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_print_stmt(self, stmt: Stmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_return_stmt(self, stmt: Stmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_var_stmt(self, stmt: Stmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_while_stmt(self, stmt: Stmt) -> Optional[Any]:
        raise NotImplemented
