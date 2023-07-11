"""
INTERPRETER
Interpret a collection of Lox expressions

"""

from typing import Any, Optional, Union
from loxpy.token import Token, TokenType
from loxpy.expr import (
    Expr,
    BinaryExpr,
    LiteralExpr,
    GroupingExpr,
    UnaryExpr
)


class InterpreterError(Exception):
    def __init__(self, token: Token, msg: str) -> None:
        super(InterpreterError, self).__init__(msg)
        self.token = token
        self.message = msg

class LoxRuntimeError(Exception):
    def __init__(self, token: Token, msg: str) -> None:
        super(LoxRuntimeError, self).__init__(msg)
        self.token = token
        self.message = msg


class Interpreter:
    def __init__(self, verbose:bool=False) -> None:
        self.verbose:bool = verbose

    def is_true(self, expr: Expr) -> bool:
        """
        Implement Ruby-style truth (False and None are false,
        others are true)
        """

        if expr is None:
            return False

        if isinstance(expr, LiteralExpr):
            return expr.value

        return True

    def is_equal(self, a:Any, b:Any) -> bool:
        if(a is None) and (b is None):
            return True
        if a is None:
            return False

        return a == b

    # TODO: revise this implementation
    def evaluate(self, expr) -> Optional[Token]:
        if self.verbose:
            print(f"Evaluating {expr}")

        if isinstance(expr, Expr):
            return expr.accept(self)  # TODO: sus
        if isinstance(expr, Token):
            return expr

        # unreachable?
        return None

    def check_number_operand(self, operator: Token, operand: Token) -> None:
        if operand.token_type != TokenType.NUMBER:
            raise LoxRuntimeError(operator, 'Operand must be a number')

    def check_number_operands(self, operator: Token, left: Token, right: Token) -> None:
        if left.token_type != TokenType.NUMBER:
            raise LoxRuntimeError(operator, f"Left operand to [{operator.lexeme}] must be a number")
        if right.token_type != TokenType.NUMBER:
            raise LoxRuntimeError(operator, f"Right operand to [{operator.lexeme}] must be a number")

    # ======== Visitor functions ======== ##
    def visit_literal_expr(self, expr: LiteralExpr) -> Expr:
        return expr.value

    def visit_grouping_expr(self, expr: GroupingExpr) -> Expr:
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: UnaryExpr) -> Union[float, bool, None]:
        right = self.evaluate(expr.right)
        if right is None:
            raise TypeError('Incorrect expression for right operand of unary expression [visit_unary_expr()]')

        #self.check_number_operand(expr.op, right)

        if right.token_type == TokenType.MINUS:
            return -float(right.lexeme)        # I presume this is what we want rather than the lexeme
        elif right.token_type == TokenType.BANG:
            return not self.is_true(right)

        # Unreachable ?
        return None

    def visit_binary_expr(self, expr: BinaryExpr) -> Union[float, None]:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        self.check_number_operands(expr.op, left, right)

        if expr.op.token_type == TokenType.MINUS:
            self.check_number_operands(expr.op, left, right)
            return float(left.lexeme) - float(right.lexeme)
        elif expr.op.token_type == TokenType.SLASH:
            return float(left.lexeme) / float(right.lexeme)
        elif expr.op.token_type == TokenType.STAR:
            return float(left.lexeme) * float(right.lexeme)
        elif expr.op.token_type == TokenType.PLUS:
            pass
        elif expr.op.token_type == TokenType.GREATER:
            return float(left.lexeme) > float(right.lexeme)
        elif expr.op.token_type == TokenType.GREATER_EQUAL:
            return float(left.lexeme) >= float(right.lexeme)
        elif expr.op.token_type == TokenType.LESS:
            return float(left.lexeme) < float(right.lexeme)
        elif expr.op.token_type == TokenType.LESS_EQUAL:
            return float(left.lexeme) <= float(right.lexeme)
        elif expr.op.token_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.op.token_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        # unreachable?
        return None

    # Entry point method
    def interpret(self, expr: Expr) -> Optional[Expr]:
        """
        INTERPRET
        Interpret the Lox expression expr
        """
        try:
            value = self.evaluate(expr)
            if self.verbose:
                print(str(value))

            return value

        except Exception as e:
            print('Interpreting error [%s]' % str(e)) #TODO : hook up the proper logging
            return None
