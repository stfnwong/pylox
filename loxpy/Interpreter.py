"""
INTERPRETER
Interpret a collection of Lox expressions

Stefan Wong 2018
"""
from typing import Type
from typing import Union

from loxpy import Token
from loxpy import Expression


class InterpreterError(Exception):
    def __init__(self, token:Type[Token.Token], msg:str) -> None:
        self.token   :Type[Token.Token] = token
        self.message :str               = msg


class Interpreter:
    def __init__(self) -> None:
        pass

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

    def evaluate(self, expr) -> Union[Token.Token, None]:
        if issubclass(type(expr), Expression.Expression):
            return expr.accept(self)
        if isinstance(expr, Token.Token):
            return expr

        return None

    # ======== Visitor functions ======== ##
    def visit_literal_expr(self, expr:Type[Expression.Expression]) -> Type[Expression.Expression]:
        return expr.value()

    def visit_grouping_expr(self, expr:Type[Expression.Expression]) -> Type[Expression.Expression]:
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr:Type[Expression.Expression]) -> Union[float, bool, None]:
        right = self.evaluate(expr.right)
        if type(right) is None:
            raise TypeError('Incorrect expression for right operand of unary expression [visit_unary_expr()]')

        if right.token_type == Token.MINUS:
            return -float(right.literal)        # I presume this is what we want rather than the lexeme
        elif right.token_type == Token.BANG:
            return not self.is_true(right)

        # Unreachable ?
        return None

    # Entry point method
    def interpret(self, expr:Type[Expression.Expression]) -> None:
        """
        INTERPRET
        Interpret the Lox expression expr
        """
        try:
            value = self.evaluate(expr)
            print(str(value))
        except:     # TODO : Create some exceptions to catch>
            print('Interpreting error') #TODO : hook up the proper logging
