# Statically _resolve variables

from typing import Sequence, Union
from collections import deque

from loxpy.error import LoxInterpreterError
from loxpy.token import Token
from loxpy.interpreter import Interpreter
from loxpy.expr import (
    Expr, 
    BinaryExpr,
    CallExpr,
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
    PrintStmt,
    ReturnStmt,
    VarStmt,
    WhileStmt
)


# For resolving variables we only care about
#
# Block Statements - these introduce a new scope for any contained variables 
# Function Declarations - these introduce a new scope for the function body and 
#   bind parameters inside that scope.
# Variable Declarations - these add a new variable to the current scope.
# Variable and Assignment Expressions - these need to have their variables _resolved.


class Resolver:
    def __init__(self, interp: Interpreter):
        self.interp = interp
        self.scopes = deque()       # Each element is Dict[str, bool] 

    def _begin_scope(self) -> None:
        self.scopes.append({})

    def _end_scope(self) -> None:
        self.scopes.pop()

    def _declare(self, name: Token) -> None:
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        scope[name.lexeme] = False   # mark as not ready

    def _define(self, name: Token) -> None:
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        scope[name.lexeme] = True   # mark as defined

    # ==== Expression visitors ==== 
    def visit_binary_expr(self, expr: BinaryExpr) -> None:
        self._resolve_expr(expr.left)
        self._resolve_expr(expr.right)

    def visit_call_expr(self, expr: CallExpr) -> None:
        self._resolve_expr(expr.callee)
        
        for arg in expr.arguments:
            self._resolve_expr(arg)

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
        #if self.scopes and self.scopes[-1][expr.name.lexeme] is False:
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
        self._resolve_function(stmt)

    def visit_if_stmt(self, stmt: IfStmt) -> None:
        self._resolve_expr(stmt.condition)
        self._resolve_stmt(stmt.then_branch)
        if stmt.else_branch is not None:
            self._resolve_stmt(stmt.else_branch)

    def visit_block_stmt(self, stmt: BlockStmt) -> None:
        self._begin_scope()
        self.resolve(stmt.stmts)
        self._end_scope()

    def visit_print_stmt(self, stmt: PrintStmt) -> None:
        self._resolve_expr(stmt.expr)

    def visit_var_stmt(self, stmt: VarStmt) -> None:
        self._declare(stmt.name)
        if stmt.initializer is not None:
            self._resolve_expr(stmt.initializer)
        
        self._define(stmt.name)

    def visit_return_stmt(self, stmt: ReturnStmt) -> None:
        if stmt.value is not None:
            self._resolve_expr(stmt.value)

    def visit_while_stmt(self, stmt: WhileStmt) -> None:
        self._resolve_expr(stmt.condition)
        self._resolve_stmt(stmt.body)

    # In Java/C++ we can do name overloads.... what is the python equivalent? 
    # Just overload the type and do isinstance?
    def _resolve_one(self, one: Union[Expr, Stmt]) -> None:
        one.accept(self)

    def _resolve_expr(self, expr: Expr) -> None:
        expr.accept(self)

    def _resolve_stmt(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def _resolve_local(self, expr: Expr, name: Token) -> None:
        print(f"Resolver._resolve_local(): resolving {expr}...")
        for depth, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interp.resolve(expr, depth)
                return

        #for idx in range(len(self.scopes)-1, -1, -1):
        #    if name.lexeme in self.scopes[idx]:
        #        self.interp.resolve(expr, len(self.scopes) - idx - 1)
        #        return

    def _resolve_function(self, func: FuncStmt) -> None:
        self._begin_scope()

        for param in func.params:
            self._declare(param)
            self._define(param)

        self.resolve(func.body)
        self._end_scope()

    def resolve(self, stmts: Sequence[Stmt]) -> None:
        for stmt in stmts:
            self._resolve_stmt(stmt)

