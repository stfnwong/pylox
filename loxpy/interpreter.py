"""
INTERPRETER
Interpret a collection of Lox expressions

"""

from typing import Any, Optional, Sequence, Union

from loxpy.token import Token, TokenType
from loxpy.expr import (
    Expr,
    BinaryExpr,
    CallExpr,
    LiteralExpr,
    LogicalExpr,
    GroupingExpr,
    UnaryExpr,
    VarExpr,
    AssignmentExpr
)

from loxpy.statement import (
    Stmt,
    ExprStmt,
    FuncStmt,
    IfStmt,
    PrintStmt,
    ReturnStmt,
    VarStmt,
    BlockStmt,
    WhileStmt
)

from loxpy.environment import Environment
from loxpy.callable import LoxCallable, LoxFunction, LoxReturnException
from loxpy.error import LoxRuntimeError

from loxpy.builtins import BUILTIN_MAP


def load_builtins() -> Environment:
    env = Environment()
    for name, func in BUILTIN_MAP.items():
        env.define(name, func)

    return env



class Interpreter:
    def __init__(self, verbose: bool=False) -> None:
        self.verbose: bool = verbose
        self.globals = load_builtins()
        self.environment = self.globals

    def is_true(self, expr: Optional[Union[Expr, bool]]) -> bool:
        """
        Implement Ruby-style truth (False and None are false,
        others are true)
        """

        if expr is None or expr is False:
            return False

        if isinstance(expr, LiteralExpr):
            return True if (expr.value and expr.value.token_type != TokenType.NIL) else False

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

    def check_number_operand(self, operator: Token, operand: Union[Token, float, bool]) -> None:
        # Check if operand is a Token then it can be a number or a boolean
        if isinstance(operand, Token):
            if operand.token_type not in (TokenType.NUMBER, TokenType.TRUE, TokenType.FALSE):
                raise LoxRuntimeError(operator, 'Operand must be a number or boolean')
        else:
            # Can also be a python number or boolean
            if not (isinstance(operand, float) or isinstance(operand, bool)):
                raise LoxRuntimeError(operator, 'Operand must be a number or boolean')

    def check_number_operands(self, operator: Token, left: Union[Token, float], right: Union[Token, float]) -> None:
        if not isinstance(left, float) and left.token_type != TokenType.NUMBER:
            raise LoxRuntimeError(operator, f"Left operand to [{operator.lexeme}] must be a number")
        if not isinstance(right, float) and right.token_type != TokenType.NUMBER:
            raise LoxRuntimeError(operator, f"Right operand to [{operator.lexeme}] must be a number")

    # ======== Visit expressions ======== ##
    def visit_literal_expr(self, expr: LiteralExpr) -> Token:
        return expr.value

    def visit_logical_expr(self, expr: LogicalExpr) -> Any:
        left = self.evaluate(expr.left)

        if expr.op.token_type == TokenType.OR:
            if self.is_true(expr.left):
                return left
        else:
            if not self.is_true(expr.left):
                return left

        return self.evaluate(expr.right)

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

    def visit_binary_expr(self, expr: BinaryExpr) -> Union[Token, float, bool, str, None]:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        # The '+' operator should also work for strings
        # TODO: re-visit this method as it seems sus...
        if isinstance(left, Token) and isinstance(right, Token) and left.token_type == TokenType.STRING and right.token_type == TokenType.STRING:
               if expr.op.token_type == TokenType.PLUS:
                   s = left.literal + right.literal
                   return Token(TokenType.STRING, s, s, left.line)

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

    def visit_call_expr(self, expr: CallExpr) -> Any:
        function = self.evaluate(expr.callee)

        if not isinstance(function, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions")

        args = []
        for arg in expr.arguments:
            args.append(self.evaluate(arg))

        if len(args) != function.arity():
            raise LoxRuntimeError(expr.paren, f"Expected {function.arity()} arguments, got {len(args)}")

        try:
            return function.call(self, args)
        except (NotImplementedError, TypeError, ValueError) as e:
            raise LoxRuntimeError(expr.paren, str(e))

    def visit_var_expr(self, expr: VarExpr) -> Any:
        return self.environment.get(expr.name)

    def visit_assignment_expr(self, expr: AssignmentExpr) -> Any:
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)

        return value

    # ======== Visit statements ======== ##
    def visit_expr_stmt(self, stmt: ExprStmt) -> Any:
        return self.evaluate(stmt.expr)

    def visit_func_stmt(self, stmt: FuncStmt) -> Any:
        func = LoxFunction(stmt)
        self.environment.define(stmt.name.lexeme, func)

    def visit_print_stmt(self, stmt: PrintStmt) -> Any:
        value = self.evaluate(stmt.expr)
        print(f"{value}")
        return value

    def visit_return_stmt(self, stmt: ReturnStmt) -> None:
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        else:
            value = None

        raise LoxReturnException(value)

    def visit_if_stmt(self, stmt: IfStmt) -> Any:
        if self.is_true(self.evaluate(stmt.condition)):
            return self.execute(stmt.then_branch)
        elif stmt.else_branch:
            return self.execute(stmt.else_branch)

        return None

    def visit_var_stmt(self, stmt: VarStmt) -> None:
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        else:
            value = None

        self.environment.define(stmt.name.lexeme, value)

    # NOTE that I am returning all the results, which is not what the interpreter does in the book
    def visit_block_stmt(self, stmt: BlockStmt) -> Sequence[Any]:
        return self.execute_block(stmt.stmts, Environment(self.environment))

    # NOTE: still returning results, ret here is a hack to maintain the pattern but
    # it will only reuturn the last result.
    def visit_while_stmt(self, stmt: WhileStmt) -> Any:
        ret = None
        while self.is_true(self.evaluate(stmt.condition)):
            ret = self.execute(stmt.body)

        return ret

    # ======== Run ======== ##
    def execute(self, stmt: Stmt) -> Any:
        return stmt.accept(self)

    def execute_block(self, stmts: Sequence[Stmt], env: Environment) -> Any:
        prev_env = self.environment
        ret = []

        try:
            self.environment = env
            for stmt in stmts:
                ret.append(self.execute(stmt))
        finally:
            self.environment = prev_env

        return ret

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
            print(f"Got runtime error [{e.message}] at {e.token} (line {e.token.line})")
            return out_stmts            # TODO: this isn't actually a useful thing to do I think

        return out_stmts

