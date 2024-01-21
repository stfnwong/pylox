# Visitor ABC
from abc import ABC, abstractmethod
from typing import Any, Optional

from loxpy.expr import (
    BinaryExpr,
    CallExpr,
    GetExpr,
    SetExpr,
    ThisExpr,
    SuperExpr,
    LiteralExpr,
    LogicalExpr,
    GroupingExpr,
    UnaryExpr,
    VarExpr,
    AssignmentExpr
)

from loxpy.statement import (
    ExprStmt,
    FuncStmt,
    IfStmt,
    PrintStmt,
    ReturnStmt,
    VarStmt,
    BlockStmt,
    ClassStmt,
    WhileStmt
)


class Visitor(ABC):

    # ======== Expression Visitors ======== #
    @abstractmethod
    def visit_assignment_expr(self, expr: AssignmentExpr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_binary_expr(self, expr: BinaryExpr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_call_expr(self, expr: CallExpr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_get_expr(self, expr: GetExpr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_grouping_expr(self, expr: GroupingExpr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_literal_expr(self, expr: LiteralExpr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_logical_expr(self, expr: LogicalExpr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_set_expr(self, expr: SetExpr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_super_expr(self, expr: SuperExpr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_this_expr(self, expr: ThisExpr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_unary_expr(self, expr: UnaryExpr) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_var_expr(self, expr: VarExpr) -> Optional[Any]:
        raise NotImplemented

    # ======== Statement Visitors ======== #
    @abstractmethod
    def visit_block_stmt(self, stmt: BlockStmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_class_stmt(self, stmt: ClassStmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_expr_stmt(self, stmt: ExprStmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_func_stmt(self, stmt: FuncStmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_if_stmt(self, stmt: IfStmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_print_stmt(self, stmt: PrintStmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_return_stmt(self, stmt: ReturnStmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_var_stmt(self, stmt: VarStmt) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    def visit_while_stmt(self, stmt: WhileStmt) -> Optional[Any]:
        raise NotImplemented
