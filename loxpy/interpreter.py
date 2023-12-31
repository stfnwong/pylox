"""
INTERPRETER
Interpret a collection of Lox expressions

"""

from typing import Any, Sequence, Union

from loxpy.token import Token, TokenType
from loxpy.expr import (
    Expr,
    BinaryExpr,
    LiteralExpr,
    GroupingExpr,
    UnaryExpr,
    VarExpr,
    AssignmentExpr
)
from loxpy.statement import (
    Stmt,
    ExprStmt,
    PrintStmt,
    VarStmt
)
from loxpy.environment import Environment
from loxpy.error import LoxRuntimeError



class Interpreter:
    def __init__(self, verbose:bool=False) -> None:
        self.verbose:bool = verbose
        self.environment = Environment()

    def is_true(self, expr: Expr) -> bool:
        """
        Implement Ruby-style truth (False and None are false,
        others are true)
        """

        if expr is None:
            return False

        if isinstance(expr, LiteralExpr):
            return True if expr.value else False

        return True

    def is_equal(self, a: Any, b: Any) -> bool:
        if(a is None) and (b is None):
            return True
        if a is None:
            return False

        return a == b

    # NOTE: Original implementation returns a LoxObject (strictly a Java Object)
    def evaluate(self, expr) -> Any:
        if self.verbose:
            print(f"Evaluating {expr}")

        if isinstance(expr, Expr):
            return expr.accept(self)

        if isinstance(expr, Token):
            return expr

        # TODO: unreachable?
        return None

    def check_number_operand(self, operator: Token, operand: Union[Token, float]) -> None:
        if not isinstance(operand, float) and operand.token_type != TokenType.NUMBER:
            raise LoxRuntimeError(operator, 'Operand must be a number')

    def check_number_operands(self, operator: Token, left: Union[Token, float], right: Union[Token, float]) -> None:
        if not isinstance(left, float) and left.token_type != TokenType.NUMBER:
            raise LoxRuntimeError(operator, f"Left operand to [{operator.lexeme}] must be a number")
        if not isinstance(right, float) and right.token_type != TokenType.NUMBER:
            raise LoxRuntimeError(operator, f"Right operand to [{operator.lexeme}] must be a number")

    # ======== Visit expressions ======== ##
    def visit_literal_expr(self, expr: LiteralExpr) -> Token:
        return expr.value

    def visit_grouping_expr(self, expr: GroupingExpr) -> Expr:
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: UnaryExpr) -> Union[float, bool, None]:
        right = self.evaluate(expr.right)
        if right is None:
            raise TypeError('Incorrect expression for right operand of unary expression [visit_unary_expr()]')

        self.check_number_operand(expr.op, right)
        
        if expr.op.token_type == TokenType.MINUS:
            if isinstance(right, Token):
                right = float(right.lexeme)
            return -right
        elif expr.op.token_type == TokenType.BANG:
            return not self.is_true(right)

        # Unreachable ?
        return None

    def visit_binary_expr(self, expr: BinaryExpr) -> Union[float, bool, None]:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        self.check_number_operands(expr.op, left, right)

        if isinstance(left, Token):
            left = float(left.lexeme)
        if isinstance(right, Token):
            right = float(right.lexeme)

        if expr.op.token_type == TokenType.MINUS:
            return left - right
        elif expr.op.token_type == TokenType.SLASH:
            return left / right
        elif expr.op.token_type == TokenType.STAR:
            return left * right
        elif expr.op.token_type == TokenType.PLUS:
            return left + right
        elif expr.op.token_type == TokenType.GREATER:
            return left > right
        elif expr.op.token_type == TokenType.GREATER_EQUAL:
            return left >= right
        elif expr.op.token_type == TokenType.LESS:
            return left < right
        elif expr.op.token_type == TokenType.LESS_EQUAL:
            return left <= right
        elif expr.op.token_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.op.token_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        # unreachable?
        return None

    def visit_var_expr(self, expr: VarExpr) -> Any:
        return self.environment.get(expr.name)

    def visit_assignment_expr(self, expr: AssignmentExpr) -> Any:
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)

        return value

    # ======== Visit statements ======== ##
    def visit_expr_stmt(self, stmt: ExprStmt) -> Any:
        return self.evaluate(stmt.expr)

    def visit_print_stmt(self, stmt: PrintStmt) -> Any:
        value = self.evaluate(stmt.expr)
        print(f"{value}")
        return value

    def visit_var_stmt(self, stmt: VarStmt) -> None:
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        else:
            value = None

        self.environment.define(stmt.name.lexeme, value)

    # ======== Run ======== ##
    def execute(self, stmt: Stmt) -> Any:
        #from pudb import set_trace; set_trace()
        return stmt.accept(self)

    # Entry point method
    def interpret(self, stmts: Sequence[Stmt]) -> Sequence[Any]:
        """
        Interpret a Sequence of Lox Statements
        """

        # TODO: note that you aren't really supposed to do this, the design is more aimed at being a
        # REPL than it is about being a module, I just find this design easier to test.
        out_stmts = []  

        try:
            for stmt in stmts:
                out_stmts.append(self.execute(stmt))
        except LoxRuntimeError as e:
            print(f"Got runtime error [{e.message}] at {e.token}")
            return out_stmts            # TODO: this isn't actually a useful thing to do I think

        return out_stmts

