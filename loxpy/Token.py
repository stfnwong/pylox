"""
TOKEN
Methods and classes for dealing with Tokens

Stefan Wong 2018
"""

# Make tokens into an enum (transform to a dict indexed by an integer

# single character tokens
(
LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE, COMMA, DOT,
MINUS, PLUS, SEMICOLON, SLASH, STAR,
# 1-2 character tokens
BANG, BANG_EQUAL, EQUAL_EQUAL, EQUAL, GREATER, GREATER_EQUAL, LESS, LESS_EQUAL,
# literals
IDENTIFIER, STRING, NUMBER,
# Keywords
AND, CLASS, ELSE, FALSE, FUN, FOR, IF, NIL, OR,
PRINT, RETURN, SUPER, THIS, TRUE, VAR, WHILE,
# EFO
LOX_EOF
) = (x for x in range(39))

TOKEN_MAP = {
    # Single character tokens
    LEFT_PAREN    : "LEFT_PAREN",
    RIGHT_PAREN   : "RIGHT_PAREN",
    LEFT_BRACE    : "LEFT_BRACE",
    RIGHT_BRACE   : "RIGHT_BRACE",
    COMMA         : "COMMA",
    DOT           : "DOT",
    MINUS         : "MINUS",
    PLUS          : "PLUS",
    SEMICOLON     : "SEMICOLON",
    SLASH         : "SLASH",
    STAR          : "STAR",
    # 1-2 character tokens
    BANG          : "BANG",
    BANG_EQUAL    : "BANG_EQUAL",
    EQUAL_EQUAL   : "EQUAL_EQUAL",
    EQUAL         : "EQUAL",
    GREATER       : "GREATER",
    GREATER_EQUAL : "GREATER_EQUAL",
    LESS          : "LESS",
    LESS_EQUAL    : "LESS_EQUAL",
    # literals
    IDENTIFIER    : "IDENTIFIER",
    STRING        : "STRING",
    NUMBER        : "NUMBER",
    # Keywords
    AND           : "AND",
    CLASS         : "CLASS",
    ELSE          : "ELSE",
    FALSE         : "FALSE",
    FUN           : "FUN",
    FOR           : "FOR",
    IF            : "IF",
    NIL           : "NIL",
    OR            : "OR",
    PRINT         : "PRINT",
    RETURN        : "RETURN",
    SUPER         : "SUPER",
    THIS          :" THIS",
    TRUE          : "TRUE",
    VAR           : "VAR",
    WHILE         : "WHILE",
    LOX_EOF       : "EOF"
}

TOKEN_SYMBOL = {
    LEFT_PAREN    : "(",
    RIGHT_PAREN   : ")",
    LEFT_BRACE    : "{",
    RIGHT_BRACE   : "}",
    COMMA         : ",",
    DOT           : ".",
    MINUS         : "-",
    PLUS          : "+",
    SEMICOLON     : ";",
    SLASH         : "/",
    STAR          : "*",
    # 1-2 character tokens
    BANG          : "!",
    BANG_EQUAL    : "!=",
    EQUAL_EQUAL   : "==",
    EQUAL         : "=",
    GREATER       : ">",
    GREATER_EQUAL : ">=",
    LESS          : "<",
    LESS_EQUAL    : "<=",
    # Keywords
    AND           : "and",
    CLASS         : "class",
    ELSE          : "else",
    FALSE         : "false",
    FUN           : "fun",
    FOR           : "for",
    IF            : "if",
    NIL           : "nil",
    OR            : "or",
    PRINT         : "print",
    RETURN        : "return",
    SUPER         : "super",
    THIS          :" this",
    TRUE          : "true",
    VAR           : "var",
    WHILE         : "while",
    LOX_EOF       : "EOF"

}

class Token(object):
    def __init__(self, token_type, lexeme, literal, line):
        if type(lexeme) is not str:
            raise ValueError("Lexeme must be a string")
        if type(line) is not int:
            raise ValueError("line must be an int")

        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        s = []
        if self.literal is None:
            s.append('%s %s line: %s\n' % (TOKEN_MAP[self.token_type], self.lexeme, self.line))
        else:
            s.append('%s %s %s line: %s\n' % (TOKEN_MAP[self.token_type], self.lexeme, self.literal, self.line))

        return ''.join(s)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.token_type != other.token_type:
            return False
        return self.__dict__  == other.__dict__
