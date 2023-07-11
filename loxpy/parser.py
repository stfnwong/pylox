"""
PARSER

Stefan Wong 2018
"""

from typing import List, TypeVar
from loxpy.expr import (
    BinaryExpr,
    Expr,
    LiteralExpr,
    UnaryExpr
)
from loxpy.token import Token, TokenType


E = TypeVar("E", covariant=True, bound=Expr | BinaryExpr | LiteralExpr | UnaryExpr)


# ParseError exception
class ParseError(Exception):
    def __init__(self, expr: Expr, msg:str) -> None:
        self.expression :Expr = expr
        self.message    :str = msg


class Parser:
    def __init__(self, token_list: List[Token]) -> None:
        if type(token_list) is not list:
            raise TypeError('token_list must be a list')
        self.token_list :list = token_list
        self.current    :int  = 0

    def __str__(self) -> str:
        s = []
        for n, t in enumerate(self.token_list):
            s.append('%4d: %s\n' % (n, str(t)))

        return ''.join(s)

    # Methods for seeking through the token list
    def _advance(self) -> Token:
        if self._at_end() is False:
            self.current += 1
        return self._previous()

    def _at_end(self) -> bool:
        cur_token = self._peek()
        if cur_token.token_type == TokenType.LOX_EOF:
            return True
        return False

    def _check(self, token_type) -> bool:
        if self._at_end():
            return False

        cur_token = self._peek()
        if cur_token.token_type == token_type:
            return True
        return False

    def _consume(self, token_type: int, msg:str) -> Token:
        if self._check(token_type):
            return self._advance()

        raise ParseError(self._peek(), msg)

    def _peek(self) -> Token:
        return self.token_list[self.current]

    def _previous(self) -> Token:
        return self.token_list[self.current - 1]

    # Methods that implement rules for productions
    def _match(self, token_types):
        for t in token_types:
            if self._check(t):
                self._advance()
                return True

        return False

    def _equality(self) -> Expr:
        expr = self._comparison()

        eq_tokens = [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]
        while self._match(eq_tokens):
            operator = self._previous()
            right = self._comparison()
            expr = BinaryExpr(operator, expr, right)

        return expr

    def _expression(self) -> Expr:
        return self._equality()

    def _comparison(self) -> BinaryExpr:
        expr = self._addition()
        comp_tokens = [TokenType.GREATER, TokenType.GREATER_EQUAL,
                       TokenType.LESS, TokenType.LESS_EQUAL]

        while self._match(comp_tokens):
            operator = self._previous()
            right    = self._addition()
            expr     = BinaryExpr(operator, expr, right)

        return expr

    def _addition(self) -> BinaryExpr:
        expr = self._multiplication()
        add_tokens = [TokenType.MINUS, TokenType.PLUS]

        while self._match(add_tokens):
            operator = self._previous()
            right    = self._multiplication()
            expr     = BinaryExpr(operator, expr, right)

        return expr

    def _multiplication(self) -> BinaryExpr:
        expr = self._unary()
        mul_tokens = [TokenType.SLASH, TokenType.STAR]

        while self._match(mul_tokens):
            operator = self._previous()
            right = self._unary()
            expr = BinaryExpr(operator, expr, right)

        return expr

    def _unary(self) -> UnaryExpr:
        un_tokens = [TokenType.BANG, TokenType.MINUS]
        if self._match(un_tokens):
            operator = self._previous()
            right = self._unary()
            expr = UnaryExpr(operator, right)
            return expr

        return self._primary()

    def _primary(self) -> LiteralExpr:
        if self._match([TokenType.FALSE]):
            expr = LiteralExpr(False)
            return expr

        if self._match([TokenType.TRUE]):
            expr = LiteralExpr(True)
            return expr

        if self._match([TokenType.NIL]):
            expr = LiteralExpr(None)
            return expr

        if self._match([TokenType.NUMBER, TokenType.STRING]):
            expr = LiteralExpr(self._previous())
            return expr

        if self._match([TokenType.LEFT_PAREN]):
            expr = LiteralExpr(None)     # TODO: incomplete
            return expr

    def parse(self) -> Expr:
        """
        Parse an expression
        """

        #statements = []
        try:
            return self._expression()
        except ParseError as e:
            print('Parse error for expression %s (%s)' % (e.expression, e.message))
            raise

