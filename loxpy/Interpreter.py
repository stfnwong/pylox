"""
INTERPRETER
Interpret a collection of Lox expressions

Stefan Wong 2018
"""

from typing import Any
from typing import Type
from typing import Union

from loxpy import Token
from loxpy import Expression


class InterpreterError(Exception):
    def __init__(self, token:Type[Token.Token], msg:str) -> None:
        super(InterpreterError, self).__init__(msg)
        self.token   :Type[Token.Token] = token
        self.message :str               = msg

class LoxRuntimeError(Exception):
    def __init__(self, Token:Type[Token.Token], msg:str) -> None:
        super(LoxRuntimeError, self).__init__(msg)
        self.token   :Type[Token.Token] = token
        self.message :str               = msg


class Interpreter:
    def __init__(self, verbose:bool=False) -> None:
        self.verbose:bool = verbose

    def is_true(self, expr:Union[None, Expression.Expression]) -> bool:
        """
        Implement Ruby-style truth (False and None are false,
        others are true)
        """
        if expr is None:
            return False

        if hasattr(expr, 'value') and isinstance(expr.value, bool):
            return expr.value

        return True

    def is_equal(self, a:Any, b:Any) -> bool:
        if(a is None) and (b is None):
            return True
        if a is None:
            return False

        return a == b

    def evaluate(self, expr) -> Union[Token.Token, None]:
        print('Evaluating expression of type %s' % str(type(expr)))
        if isinstance(expr, Expression.Expression):
            return expr.accept(self)
        if isinstance(expr, Token.Token):
            return expr

        return None

    def check_number_operand(self, operator:Token.Token, operand:float) -> None:
        if not isinstance(operand, float) or not isinstance(operand, int):
            raise LoxRuntimeError('Operand must be a number')

    def check_number_operands(self, operator:Token.Token, left:float, right:float) -> None:
        if not isinstance(left, float) or isinstance(right, float):
            raise LoxRuntimeError('Left operand must be a number')

        if not isinstance(right, float) or isinstance(right, float):
            raise LoxRuntimeError('Right operand must be a number')

    # ======== Visitor functions ======== ##
    def visit_literal_expr(self, expr:Type[Expression.Expression]) -> Type[Expression.Expression]:
        return expr.value()

    def visit_grouping_expr(self, expr:Type[Expression.Expression]) -> Type[Expression.Expression]:
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr:Type[Expression.Expression]) -> Union[float, bool, None]:
        right = self.evaluate(expr.right)
        if right is None:
            raise TypeError('Incorrect expression for right operand of unary expression [visit_unary_expr()]')

        self.check_number_operand(expr.op, right)

        if right.token_type == Token.MINUS:
            return -float(right.lexeme)        # I presume this is what we want rather than the lexeme
        elif right.token_type == Token.BANG:
            return not self.is_true(right)

        # Unreachable ?
        return None

    def visit_binary_expr(self, expr:Type[Expression.Expression]) -> Union[float, None]:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        self.check_number_operands(expr.op, left, right)

        if expr.op.token_type == Token.MINUS:
            self.check_number_operands(expr.op, left, right)
            return float(left.lexeme) - float(right.lexeme)
        elif expr.op.token_type == Token.SLASH:
            return float(left.lexeme) / float(right.lexeme)
        elif expr.op.token_type == Token.STAR:
            return float(left.lexeme) * float(right.lexeme)
        elif expr.op.token_type == Token.PLUS:
            pass
        elif expr.op.token_type == Token.GREATER:
            return float(left.lexeme) > float(right.lexeme)
        elif expr.op.token_type == Token.GREATER_EQUAL:
            return float(left.lexeme) >= float(right.lexeme)
        elif expr.op.token_type == Token.LESS:
            return float(left.lexeme) < float(right.lexeme)
        elif expr.op.token_type == Token.LESS_EQUAL:
            return float(left.lexeme) <= float(right.lexeme)
        elif expr.op.token_type == Token.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.op.token_type == Token.EQUAL_EQUAL:
            return self.is_equal(left, right)

        # unreachable?
        return None

    # Entry point method
    def interpret(self, expr:Type[Expression.Expression]) -> Union[Expression.Expression, None]:
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
