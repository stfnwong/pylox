"""
PARSER

Implements parsing for the Lox language.
"""

from typing import List, Sequence, Optional, Union
from loxpy.expr import (
    Expr,
    AssignmentExpr,
    BinaryExpr,
    CallExpr,
    GetExpr,
    GroupingExpr,
    LiteralExpr,
    LogicalExpr,
    SetExpr,
    SuperExpr,
    ThisExpr,
    UnaryExpr,
    VarExpr,
)
from loxpy.statement import (
    Stmt, 
    BlockStmt,
    ClassStmt,
    ExprStmt, 
    FuncStmt,
    IfStmt,
    PrintStmt, 
    ReturnStmt,
    VarStmt, 
    WhileStmt
)
from loxpy.token import Token, TokenType
from loxpy.error import LoxParseError


#E = TypeVar("E", covariant=True, bound=Expr | BinaryExpr | LiteralExpr | UnaryExpr)


class Parser:
    def __init__(self, token_list: Sequence[Token]) -> None:
        if type(token_list) is not list:
            raise TypeError('token_list must be a list')
        self.token_list: Sequence[Token] = token_list
        self.current   : int  = 0
        self.max_args = 255

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

    def _check(self, token_type: TokenType) -> bool:
        if self._at_end():
            return False

        cur_token = self._peek()
        if cur_token.token_type == token_type:
            return True
        return False

    def _consume(self, token_type: TokenType, msg:str) -> Token:
        if self._check(token_type):
            return self._advance()

        raise LoxParseError(self._peek(), msg)

    def _peek(self) -> Token:
        return self.token_list[self.current]

    def _previous(self) -> Token:
        return self.token_list[self.current - 1]

    def _synchronise(self) -> None:
        self._advance()

        while not self._at_end():
            if self._previous().token_type == TokenType.SEMICOLON:
                return

            adv = (
                TokenType.CLASS,
                TokenType.FUNC,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            )
            if self._peek().token_type in adv:
                return

            self._advance()

    def _match(self, token_types: Sequence[TokenType]) -> bool:
        for t in token_types:
            if self._check(t):
                self._advance()
                return True

        return False

    # ==== Statements =====
    def _expression_statement(self) -> ExprStmt:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression")

        return ExprStmt(expr)

    # ==== Productions 
    def _expression(self) -> Expr:
        return self._assignment()

    def _assignment(self) -> Expr:
        expr = self._or()

        if self._match([TokenType.EQUAL]):
            equals = self._previous()
            value = self._assignment()

            if isinstance(expr, VarExpr):
                name = expr.name
                return AssignmentExpr(name, value)
            elif isinstance(expr, GetExpr):    # TODO: what to tell linter here?
                return SetExpr(expr.obj, expr.name, value)

            raise LoxParseError(equals, "Invalid assignment target")

        return expr

    def _and(self) -> Expr:
        expr = self._equality()

        while self._match([TokenType.AND]):
            op = self._previous()
            right = self._equality()
            expr = LogicalExpr(op, expr, right)

        return expr

    def _or(self) -> Expr:
        expr = self._and()

        while self._match([TokenType.OR]):
            op = self._previous()
            right = self._and()
            expr = LogicalExpr(op, expr, right)

        return expr

    def _function(self, kind: str) -> FuncStmt:
        name = self._consume(TokenType.IDENTIFIER, f"Expect {kind} name")
        self._consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name")
        params = []

        # Parse parameters
        if not self._check(TokenType.RIGHT_PAREN):
            params.append(self._consume(TokenType.IDENTIFIER, "Expect parameter name"))

            while self._match([TokenType.COMMA]):
                if len(params) >= self.max_args:
                    raise LoxParseError(self._peek(), f"[{kind}] can't have more than {self.max_args} parameters")
                params.append(self._consume(TokenType.IDENTIFIER, "Expect parameter name"))

        self._consume(TokenType.RIGHT_PAREN, f"Expect ')' after {kind} parameter list")

        # Now parse the function body 
        # Stupid workaround since I can't get a '{' into an f-string in a way that 
        # my tool setup will accept.
        LEFT_BRACE = "{"        
        self._consume(TokenType.LEFT_BRACE, f"Expect '{LEFT_BRACE}' before {kind} body")
        body = self._block_statement()

        return FuncStmt(name, params, body)

    def _class_decl(self) -> Stmt:
        name = self._consume(TokenType.IDENTIFIER, "Expect class name")

        # Consume the superclass, if any
        if self._match([TokenType.LESS]):
            self._consume(TokenType.IDENTIFIER, "Expect superclass name")
            superclass = VarExpr(self._previous())
        else:
            superclass = None

        self._consume(TokenType.LEFT_BRACE, "Expect '{' before class body")

        methods = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._at_end():
            methods.append(self._function("method"))

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after class body")

        return ClassStmt(name, superclass, methods)

    def _declaration(self) -> Stmt:
        try:
            if self._match([TokenType.CLASS]):
                return self._class_decl()
            if self._match([TokenType.FUNC]):
                return self._function("function")

            if self._match([TokenType.VAR]):
                return self._var_declaration()

            return self._statement()
        except LoxParseError as e:
            self._synchronise()
            raise e

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

        return self._call()

    def _finish_call(self, callee: Expr) -> Expr:
        args = []

        # If the next token is ')' then no need to parse arguments
        if not self._check(TokenType.RIGHT_PAREN):
            args.append(self._expression())
            while self._match([TokenType.COMMA]):
                if len(args) >= self.max_args:
                    raise LoxParseError(self._peek(), f"Can't have more than {self.max_args} arguments to function")
                args.append(self._expression())

        paren = self._consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments")

        return CallExpr(callee, paren, tuple(args))

    def _call(self) -> Expr:
        expr = self._primary()

        while True:
            if self._match([TokenType.LEFT_PAREN]):
                expr = self._finish_call(expr)
            elif self._match([TokenType.DOT]):
                name = self._consume(TokenType.IDENTIFIER, "Expect property name after '.'")
                expr = GetExpr(expr, name)
            else:
                break

        return expr

    def _primary(self) -> Expr:
        def token_copy(t: TokenType) -> Token:
            return Token(
                t, 
                self.token_list[-1].lexeme, 
                self.token_list[-1].literal, 
                self.token_list[-1].line, 
                self.token_list[-1].col
            )

        if self._match([TokenType.FALSE]):
            return LiteralExpr(token_copy(TokenType.FALSE))

        if self._match([TokenType.TRUE]):
            return LiteralExpr(token_copy(TokenType.TRUE))

        if self._match([TokenType.NIL]):
            return LiteralExpr(token_copy(TokenType.NIL))

        if self._match([TokenType.NUMBER, TokenType.STRING]):
            return LiteralExpr(self._previous())

        if self._match([TokenType.SUPER]):
            keyword = self._previous()
            self._consume(TokenType.DOT, "Expect '.' after 'super'")
            method = self._consume(TokenType.IDENTIFIER, "Expect superclass method name")
            return SuperExpr(keyword, method)

        if self._match([TokenType.THIS]):
            return ThisExpr(self._previous())

        if self._match([TokenType.IDENTIFIER]):
            return VarExpr(self._previous())

        if self._match([TokenType.LEFT_PAREN]):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return GroupingExpr(expr)

        return LiteralExpr(token_copy(self.token_list[-1].token_type))      # unreachable

    def _if_statement(self) -> IfStmt:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after if")
        cond = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition")

        then_branch = self._statement()
        if self._match([TokenType.ELSE]):
            else_branch = self._statement()
        else:
            else_branch = None

        return IfStmt(cond, then_branch, else_branch)

    def _for_statement(self) -> Stmt:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'")

        # Format of the for statement is 
        # for(init; cond; increment) { body }
        if self._match([TokenType.SEMICOLON]):
            init = None
        elif self._match([TokenType.VAR]):
            init = self._var_declaration()
        else:
            init = self._expr_statement()

        if not self._check(TokenType.SEMICOLON):
            cond = self._expression()
        else:
            cond = None
        self._consume(TokenType.SEMICOLON, "Expect ';' after for condition")

        if not self._check(TokenType.RIGHT_PAREN):
            increment = self._expression()
        else:
            increment = None
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after for increment")

        body = self._statement()

        if increment:
            body = BlockStmt([body, ExprStmt(increment)])

        # If we don't have a condition then we force the condition to true,
        # resulting in an infinite loop. (Future work, add break?)
        if not cond:
            cond = LiteralExpr(
                Token(TokenType.TRUE, "true", "true", self.token_list[self.current].line)
            )

        body = WhileStmt(cond, body)

        # Take the condition and the body and build a new block out of it
        if init:
            body = BlockStmt([init, body])

        return body

    def _print_statement(self) -> PrintStmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value")

        return PrintStmt(value)

    def _return_statement(self) -> ReturnStmt:
        keyword = self._previous()
        if not self._check(TokenType.SEMICOLON):
            value = self._expression()
        else:
            value = None

        self._consume(TokenType.SEMICOLON, "Expect ';' after return")

        return ReturnStmt(keyword, value)

    def _while_statement(self) -> WhileStmt:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'")
        cond = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after condition")
        body = self._statement()

        return WhileStmt(cond, body)

    def _block_statement(self) -> List[Stmt]:
        stmts = []
        
        while not self._check(TokenType.RIGHT_BRACE) and not self._at_end():
            stmts.append(self._declaration())
        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block")

        return stmts


    def _expr_statement(self) -> ExprStmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value")

        return ExprStmt(value)

    def _statement(self) -> Stmt:
        if self._match([TokenType.FOR]):
            return self._for_statement()

        if self._match([TokenType.IF]):
            return self._if_statement()

        if self._match([TokenType.PRINT]):
            return self._print_statement()

        if self._match([TokenType.RETURN]):
            return self._return_statement()

        if self._match([TokenType.WHILE]):
            return self._while_statement()

        if self._match([TokenType.LEFT_BRACE]):
            return BlockStmt(self._block_statement())

        return self._expr_statement()

    def parse(self) -> Sequence[Stmt]:
        """
        Parse an expression
        """

        statements = []

        while not self._at_end():
            statements.append(self._declaration())

        return statements

