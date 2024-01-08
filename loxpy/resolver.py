# Statically _resolve variables

from typing import Sequence, Union
from collections import deque
from enum import auto, Enum

from loxpy.error import LoxInterpreterError
from loxpy.token import Token
from loxpy.interpreter import Interpreter
from loxpy.expr import (
    Expr, 
    BinaryExpr,
    CallExpr,
    GetExpr,
    SetExpr,
    GroupingExpr,
    LiteralExpr, 
    LogicalExpr,
    UnaryExpr,
    VarExpr, 
    AssignmentExpr
)
from loxpy.statement import (
    Stmt,
    ExprStmt,
    FuncStmt,
    IfStmt,
    BlockStmt,
    ClassStmt,
    PrintStmt,
    ReturnStmt,
    VarStmt,
    WhileStmt
)


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    METHOD = auto()


# For resolving variables we only care about
#
# Block Statements - these introduce a new scope for any contained variables 
# Function Declarations - these introduce a new scope for the function body and 
#   bind parameters inside that scope.
# Variable Declarations - these add a new variable to the current scope.
# Variable and Assignment Expressions - these need to have their variables _resolved.


class Resolver:
    def __init__(self, interp: Interpreter):
        self.cur_func = FunctionType.NONE
        self.interp = interp
        # Each element in scopes is  Dict[str, List[bool, bool]]
        # where 
        # [name, [ready, used]]
        self.scopes = deque()       

    def _begin_scope(self) -> None:
        self.scopes.append({})

    def _end_scope(self) -> None:
        # Check if any vars were unused
        for name, (_, used) in self.scopes[-1].items():
            if used is False:
                print(f"WARNING: Variable [{name}] unused")

        self.scopes.pop()

    def _declare(self, name: Token) -> None:
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        if name.lexeme in scope:
            raise LoxInterpreterError(name, f"[{name.lexeme}] already in this scope")

        scope[name.lexeme] = [False, False]   # mark as not ready

    def _define(self, name: Token) -> None:
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        scope[name.lexeme] = [True, False]   # mark as defined

    # ==== Expression visitors ==== 
    def visit_binary_expr(self, expr: BinaryExpr) -> None:
        self._resolve_expr(expr.left)
        self._resolve_expr(expr.right)

    def visit_call_expr(self, expr: CallExpr) -> None:
        self._resolve_expr(expr.callee)
        
        for arg in expr.arguments:
            self._resolve_expr(arg)

    def visit_get_expr(self, expr: GetExpr) -> None:
        self._resolve_expr(expr.obj)

    def visit_set_expr(self, expr: SetExpr) -> None:
        self._resolve_expr(expr.value)
        self._resolve_expr(expr.obj)

    def visit_grouping_expr(self, expr: GroupingExpr) -> None:
        self._resolve_expr(expr.expression)

    def visit_literal_expr(self, expr: LiteralExpr) -> None:  # pylint: disable=unused-argument
        return

    def visit_logical_expr(self, expr: LogicalExpr) -> None:
        self._resolve_expr(expr.left)
        self._resolve_expr(expr.right)

    def visit_unary_expr(self, expr: UnaryExpr) -> None:
        self._resolve_expr(expr.right)
        
    def visit_var_expr(self, expr: VarExpr) -> None:
        if self.scopes and (self.scopes[-1].get(expr.name.lexeme, None) is False):
            raise LoxInterpreterError(expr.name, f"Failed to read local variable [{expr.name.lexeme}] in its own initializer")

        self._resolve_local(expr, expr.name)

    def visit_assignment_expr(self, expr: AssignmentExpr) -> None:
        self._resolve_expr(expr.value)
        self._resolve_local(expr, expr.name)

    # ==== Statement visitors ====  
    def visit_expr_stmt(self, stmt: ExprStmt) -> None:
        self._resolve_expr(stmt.expr)

    def visit_func_stmt(self, stmt: FuncStmt) -> None:
        self._declare(stmt.name)
        self._define(stmt.name)
        self._resolve_function(stmt, FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt: IfStmt) -> None:
        self._resolve_expr(stmt.condition)
        self._resolve_stmt(stmt.then_branch)
        if stmt.else_branch is not None:
            self._resolve_stmt(stmt.else_branch)

    def visit_block_stmt(self, stmt: BlockStmt) -> None:
        self._begin_scope()
        self.resolve(stmt.stmts)
        self._end_scope()

    def visit_class_stmt(self, stmt: ClassStmt) -> None:
        self._declare(stmt.name)
        self._define(stmt.name)

        for method in stmt.methods:
            self._resolve_function(method, FunctionType.METHOD)

    def visit_print_stmt(self, stmt: PrintStmt) -> None:
        self._resolve_expr(stmt.expr)

    def visit_var_stmt(self, stmt: VarStmt) -> None:
        self._declare(stmt.name)
        if stmt.initializer is not None:
            self._resolve_expr(stmt.initializer)
        
        self._define(stmt.name)

    def visit_return_stmt(self, stmt: ReturnStmt) -> None:
        if self.cur_func == FunctionType.NONE:
            raise LoxInterpreterError(stmt.keyword, "Can't return from top level")

        if stmt.value is not None:
            self._resolve_expr(stmt.value)

    def visit_while_stmt(self, stmt: WhileStmt) -> None:
        self._resolve_expr(stmt.condition)
        self._resolve_stmt(stmt.body)

    # In Java/C++ we can do name overloads.... what is the python equivalent? 
    # Just overload the type and do isinstance?
    def _resolve_expr(self, expr: Expr) -> None:
        expr.accept(self)

    def _resolve_stmt(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def _resolve_local(self, expr: Expr, name: Token) -> None:
        for depth, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interp.resolve(expr, depth)
                scope[name.lexeme][1] = True
                return

    def _resolve_function(self, func: FuncStmt, ftype: FunctionType) -> None:
        enclosing_func = self.cur_func
        self.cur_func = ftype
        self._begin_scope()

        for param in func.params:
            self._declare(param)
            self._define(param)

        self.resolve(func.body)
        self._end_scope()
        self.cur_func = enclosing_func

    def resolve(self, stmts: Sequence[Stmt]) -> None:
        for stmt in stmts:
            self._resolve_stmt(stmt)

