"""
TOKEN
"""

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
    FUN = auto()
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
    TokenType.FUN           : "FUN",
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
    TokenType.AND           : "and",
    TokenType.CLASS         : "class",
    TokenType.ELSE          : "else",
    TokenType.FALSE         : "false",
    TokenType.FUN           : "fun",
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


# TODO: re-write as dataclass
class Token:
    """
    Token.

    Represents a token in the Lox source.
    """
    def __init__(self, token_type: TokenType, lexeme:str, literal:Any, line:int) -> None:
        if type(lexeme) is not str:
            raise ValueError("Lexeme must be a string")
        if type(line) is not int:
            raise ValueError("line must be an int")

        self.token_type : TokenType = token_type
        self.lexeme     :str = lexeme
        self.literal    :Any = literal
        self.line       :int = line

    def __str__(self) -> str:
        s = []
        if self.literal is None:
            s.append('%s [%s] line: %s' % (TOKEN_MAP[self.token_type], self.lexeme, self.line))
        else:
            s.append('%s [%s] %s line: %s' % (TOKEN_MAP[self.token_type], self.lexeme, self.literal, self.line))

        return ''.join(s)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other:object) -> bool:
        if not isinstance(other, Token):
            return NotImplemented

        if self.token_type != other.token_type:
            return False

        return self.__dict__  == other.__dict__
