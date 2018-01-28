"""
INTERPRETER
Interpret a collection of Lox expressions

Stefan Wong 2018
"""

from loxpy import Token
from loxpy import Expression

class Interpreter(object):
    def __init__(self):
        pass

    def is_true(self, expr):
        """
        Implement Ruby-style truth (False and None are false,
        others are true)
        """
        if expr is None:
            return False
        if isinstance(expr.value, bool):
            return expr.value
        return True

    def evaluate(self, expr):
        if issubclass(type(expr), Expression.Expression):
            return expr.accept(self)
        return None     # TODO: what to do here?

    # Visitor functions
    def visit_literal_expr(self, expr):
        return expr.value()

    # Parenthesis
    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        if right.op.token_type == Token.MINUS:
            return -float(right.literal)        # I presume this is what we want rather than the lexeme
        elif right.op.token_type == Token.BANG:
            return not self.is_true(right)

        # Unreachable
        return None


    # Entry point method
    def interpret(self, expr):
        """
        INTERPRET
        Interpret the Lox expression expr
        """
        try:
            value = self.evaluate(expr)
            print(str(value))
        except:     # TODO : Create some exceptions to catch>
            print('Interpreting error') #TODO : hook up the proper logging
