"""
TOKEN
"""

from dataclasses import dataclass
from enum import auto, Enum
from typing import Any



class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()
    BANG = auto()
    EQUAL = auto()
    BANG_EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUNC = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    LOX_EOF = auto()


TOKEN_MAP = {
    # Single character tokens
    TokenType.LEFT_PAREN    : "LEFT_PAREN",
    TokenType.RIGHT_PAREN   : "RIGHT_PAREN",
    TokenType.LEFT_BRACE    : "LEFT_BRACE",
    TokenType.RIGHT_BRACE   : "RIGHT_BRACE",
    TokenType.COMMA         : "COMMA",
    TokenType.DOT           : "DOT",
    TokenType.MINUS         : "MINUS",
    TokenType.PLUS          : "PLUS",
    TokenType.SEMICOLON     : "SEMICOLON",
    TokenType.SLASH         : "SLASH",
    TokenType.STAR          : "STAR",
    # 1-2 character tokens
    TokenType.BANG          : "BANG",
    TokenType.BANG_EQUAL    : "BANG_EQUAL",
    TokenType.EQUAL_EQUAL   : "EQUAL_EQUAL",
    TokenType.EQUAL         : "EQUAL",
    TokenType.GREATER       : "GREATER",
    TokenType.GREATER_EQUAL : "GREATER_EQUAL",
    TokenType.LESS          : "LESS",
    TokenType.LESS_EQUAL    : "LESS_EQUAL",
    # literals
    TokenType.IDENTIFIER    : "IDENTIFIER",
    TokenType.STRING        : "STRING",
    TokenType.NUMBER        : "NUMBER",
    # Keywords
    TokenType.AND           : "AND",
    TokenType.CLASS         : "CLASS",
    TokenType.ELSE          : "ELSE",
    TokenType.FALSE         : "FALSE",
    TokenType.FUNC          : "FUNC",
    TokenType.FOR           : "FOR",
    TokenType.IF            : "IF",
    TokenType.NIL           : "NIL",
    TokenType.OR            : "OR",
    TokenType.PRINT         : "PRINT",
    TokenType.RETURN        : "RETURN",
    TokenType.SUPER         : "SUPER",
    TokenType.THIS          :" THIS",
    TokenType.TRUE          : "TRUE",
    TokenType.VAR           : "VAR",
    TokenType.WHILE         : "WHILE",
    TokenType.LOX_EOF       : "EOF"
}

TOKEN_SYMBOL = {
    TokenType.LEFT_PAREN    : "(",
    TokenType.RIGHT_PAREN   : ")",
    TokenType.LEFT_BRACE    : "{",
    TokenType.RIGHT_BRACE   : "}",
    TokenType.COMMA         : ",",
    TokenType.DOT           : ".",
    TokenType.MINUS         : "-",
    TokenType.PLUS          : "+",
    TokenType.SEMICOLON     : ";",
    TokenType.SLASH         : "/",
    TokenType.STAR          : "*",
    # 1-2 character tokens
    TokenType.BANG          : "!",
    TokenType.BANG_EQUAL    : "!=",
    TokenType.EQUAL_EQUAL   : "==",
    TokenType.EQUAL         : "=",
    TokenType.GREATER       : ">",
    TokenType.GREATER_EQUAL : ">=",
    TokenType.LESS          : "<",
    TokenType.LESS_EQUAL    : "<=",
    # Keywords
    TokenType.AND           : "and",    # NOTE: could also extend the logic operators as &&, ||, etc
    TokenType.CLASS         : "class",
    TokenType.ELSE          : "else",
    TokenType.FALSE         : "false",
    TokenType.FUNC          : "func",
    TokenType.FOR           : "for",
    TokenType.IF            : "if",
    TokenType.NIL           : "nil",
    TokenType.OR            : "or",
    TokenType.PRINT         : "print",
    TokenType.RETURN        : "return",
    TokenType.SUPER         : "super",
    TokenType.THIS          :" this",
    TokenType.TRUE          : "true",
    TokenType.VAR           : "var",
    TokenType.WHILE         : "while",
    TokenType.LOX_EOF       : "EOF"
}


@dataclass(frozen=True)
class Token:
    """
    Token.
    Represents a token in the Lox source.

    Arguments:
        token_type (TokenType): the type of this token.
        lexeme (str): The lexeme string from the source associated with this token.
        literal (Any): Any literal. Used for literal expressions.
        line (int): The line in the source file where the token was parsed.

    """

    token_type: TokenType
    lexeme: str
    literal: Any    # Later it might be worth reducing the scope of this
    line: int
    col: int = 0    # Column in source, if we know

    # NOTE: dataclass doens't seem to like having seperate __str__() and __repr__() methods
    # Ideally I'd like to keep the original __repr__ method also
    def __str__(self) -> str:
        return f"{self.lexeme}"

    def __repr__(self) -> str:
        r = ",".join(
            f"{k}={v!r}" for k, v in self.__dict__.items()
        )
        return f"{self.__class__.__name__}({r})"
