"""
PARSER

Stefan Wong 2018
"""

from typing import List, TypeVar, Optional, Union
from loxpy.expr import (
    BinaryExpr,
    Expr,
    LiteralExpr,
    UnaryExpr,
    GroupingExpr
)
from loxpy.statement import Stmt, PrintStmt, ExprStmt, VarStmt
from loxpy.token import Token, TokenType
from loxpy.error import LoxParseError


E = TypeVar("E", covariant=True, bound=Expr | BinaryExpr | LiteralExpr | UnaryExpr)


# ParseError exception
#class ParseError(Exception):
#    def __init__(self, expr: Expr, msg:str) -> None:
#        self.message    :str = msg



class Parser:
    def __init__(self, token_list: List[Token]) -> None:
        if type(token_list) is not list:
            raise TypeError('token_list must be a list')
        self.token_list: List[Token] = token_list
        self.current   : int  = 0

    def __str__(self) -> str:
        s = []
        for n, t in enumerate(self.token_list):
            s.append('%4d: %s\n' % (n, str(t)))

        return ''.join(s)

    # ==== Methods for moving through source ==== #
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

    def _consume(self, token_type: TokenType, msg:str) -> Token:
        if self._check(token_type):
            return self._advance()

        # TODO: something wrong here...
        raise LoxParseError(self._peek(), msg)

    def _peek(self) -> Token:
        return self.token_list[self.current]

    def _previous(self) -> Token:
        return self.token_list[self.current - 1]

    # Methods that implement rules for productions
    def _match(self, token_types: List[TokenType]) -> bool:
        for t in token_types:
            if self._check(t):
                self._advance()
                return True

        return False

    def _synchronise(self) -> None:
        pass

    # ==== Statements =====
    def _expression_statement(self) -> ExprStmt:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression")

        return ExprStmt(expr)

    # ==== Productions 
    def _expression(self) -> Expr:
        return self._equality()

    def _declaration(self) -> Optional[Stmt]:
        try:
            if self._match([TokenType.VAR]):
                return self._var_declaration()

            return self._statement()
        except LoxParseError as e:
            self._synchronise()
            return None

    def _var_declaration(self) -> Stmt:
        name = self._consume(TokenType.IDENTIFIER, "Expect variable name")

        if self._match([TokenType.EQUAL]):
            initializer = self._expression()
        else:
            initializer = None

        self._consume(TokenType.SEMICOLON, "Expect ';' after variable declaration")

        return VarStmt(name, initializer)


    def _equality(self) -> Expr:
        expr = self._comparison()

        eq_tokens = [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]
        while self._match(eq_tokens):
            operator = self._previous()
            right = self._comparison()
            expr = BinaryExpr(operator, expr, right)

        return expr


    def _comparison(self) -> Expr:
        expr = self._term()
        comp_tokens = [
            TokenType.GREATER, 
            TokenType.GREATER_EQUAL,
            TokenType.LESS, 
            TokenType.LESS_EQUAL
        ]

        while self._match(comp_tokens):
            operator = self._previous()
            right    = self._term()
            expr     = BinaryExpr(operator, expr, right)

        return expr

    def _term(self) -> Expr:
        expr = self._factor()
        add_tokens = [TokenType.MINUS, TokenType.PLUS]

        while self._match(add_tokens):
            operator = self._previous()
            right    = self._factor()
            expr     = BinaryExpr(operator, expr, right)

        return expr

    def _factor(self) -> Expr:
        expr = self._unary()
        mul_tokens = [TokenType.SLASH, TokenType.STAR]

        while self._match(mul_tokens):
            operator = self._previous()
            right = self._unary()
            expr = BinaryExpr(operator, expr, right)

        return expr

    def _unary(self) -> Expr:
        un_tokens = [TokenType.BANG, TokenType.MINUS]
        if self._match(un_tokens):
            operator = self._previous()
            right = self._unary()
            expr = UnaryExpr(operator, right)
            return expr

        return self._primary()

    def _primary(self) -> Union[GroupingExpr, LiteralExpr]:
        expr = LiteralExpr(
            Token(
                TokenType.NIL,
                self.token_list[-1].lexeme,
                self.token_list[-1].literal,
                self.token_list[-1].line
            )
        )

        if self._match([TokenType.FALSE]):
            expr.value.token_type = TokenType.FALSE

        if self._match([TokenType.TRUE]):
            expr.value.token_type = TokenType.TRUE

        if self._match([TokenType.NIL]):
            expr.value.token_type = TokenType.NIL

        if self._match([TokenType.NUMBER, TokenType.STRING]):
            expr = LiteralExpr(self._previous())

        if self._match([TokenType.IDENTIFIER]):
            return VarExpr(self._previous())

        if self._match([TokenType.LEFT_PAREN]):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return GroupingExpr(expr)

        return expr

    def _print_statement(self) -> PrintStmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value")
        return PrintStmt(value)

    def _expr_statement(self) -> ExprStmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value")
        return ExprStmt(value)

    def _statement(self) -> Stmt:
        if self._match([TokenType.PRINT]):
            return self._print_statement()

        return self._expr_statement()

    def parse(self) -> List[Stmt]:
        """
        Parse an expression
        """

        statements = []

        try:
            while not self._at_end():
                statements.append(self._declaration())
        except LoxParseError as e:
            # TODO: Should a ParseError hold a token or an expression?
            print(f"Parse error for expression {e.token}, ({e.message})")   
            raise

        return statements

