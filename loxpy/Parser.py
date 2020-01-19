"""
PARSER

Stefan Wong 2018
"""

from typing import List, Type
from loxpy import Expression
from loxpy import Token

# Debug
#from pudb import set_trace; set_trace()


# ParseError exception
class ParseError(Exception):
    def __init__(self, expr:Expression.Expression, msg:str) -> None:
        self.expression :Expression.Expression = expr
        self.message    :str = msg


class Parser:
    def __init__(self, token_list:List[Token.Token]) -> None:
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
    def _advance(self) -> Type[Token.Token]:     # Does not consume token
        if self._at_end() is False:
            self.current += 1
        return self._previous()

    def _at_end(self) -> bool:
        cur_token = self._peek()
        if cur_token.token_type == Token.LOX_EOF:
            return True
        return False

    def _check(self, token_type) -> bool:
        if self._at_end():
            return False

        cur_token = self._peek()
        if cur_token.token_type == token_type:
            return True
        return False

    def _consume(self, token_type:int, msg:str) -> Type[Token.Token]:
        if self._check(token_type):
            return self._advance()

        raise ParseError(self._peek(), msg)

    def _peek(self) -> Type[Token.Token]:
        return self.token_list[self.current]

    def _previous(self) -> Type[Token.Token]:
        return self.token_list[self.current - 1]

    # Methods that implement rules for productions
    def _match(self, token_types):
        for t in token_types:
            if self._check(t):
                self._advance()
                return True

        return False

    def _equality(self) -> Type[Expression.Binary]:
        expr = self._comparison()

        eq_tokens = [Token.BANG_EQUAL, Token.EQUAL_EQUAL]
        while self._match(eq_tokens):
            operator = self._previous()
            right = self._comparison()
            expr = Expression.Binary(expr, operator, right)

        return expr

    def _expression(self) -> Type[Expression.Expression]:
        return self._equality()

    def _comparison(self) -> Type[Expression.Binary]:
        expr = self._addition()
        comp_tokens = [Token.GREATER, Token.GREATER_EQUAL,
                       Token.LESS, Token.LESS_EQUAL]

        while self._match(comp_tokens):
            operator = self._previous()
            right    = self._addition()
            expr     = Expression.Binary(expr, operator, right)

        return expr

    def _addition(self) -> Type[Expression.Binary]:
        expr = self._multiplication()
        add_tokens = [Token.MINUS, Token.PLUS]

        while self._match(add_tokens):
            operator = self._previous()
            right    = self._multiplication()
            expr     = Expression.Binary(expr, operator, right)

        return expr

    def _multiplication(self) -> Type[Expression.Binary]:
        expr = self._unary()
        mul_tokens = [Token.SLASH, Token.STAR]

        while self._match(mul_tokens):
            operator = self._previous()
            right = self._unary()
            expr = Expression.Binary(expr, operator, right)

        return expr

    def _unary(self) -> Type[Expression.Unary]:
        un_tokens = [Token.BANG, Token.MINUS]
        if self._match(un_tokens):
            operator = self._previous()
            right = self._unary()
            expr = Expression.Unary(operator, right)
            return expr

        return self._primary()

    def _primary(self) -> Expression.Literal:
        if self._match([Token.FALSE]):
            expr = Expression.Literal(False)
            return expr

        if self._match([Token.TRUE]):
            expr = Expression.Literal(True)
            return expr

        if self._match([Token.NIL]):
            expr = Expression.Literal(None)
            return expr

        if self._match([Token.NUMBER, Token.STRING]):
            expr = Expression.Literal(self._previous())
            return expr

        if self._match([Token.LEFT_PAREN]):
            expr = Expression.Literal()     # <- TODO : check this
            return expr

    def parse(self) -> Type[Expression.Expression]:
        """
        Parse an expression
        """
        try:
            return self._expression()
        except ParseError as e:
            print('Parse error for expression %s (%s)' % (e.expression, e.message))
            return None

