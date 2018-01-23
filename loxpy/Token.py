"""
TOKEN
Methods and classes for dealing with Tokens

Stefan Wong 2018
"""

# Make tokens into an enum (transform to a dict indexed by an integer

# single character tokens
(
LEFT_PAREN    ,
RIGHT_PAREN   ,
LEFT_BRACE    ,
RIGHT_BRACE   ,
COMMA         ,
DOT           ,
MINUS         ,
PLUS          ,
SEMICOLON     ,
SLASH         ,
STAR          ,
# 1-2 character tokens
BANG          ,
BANG_EQUAL    ,
EQUAL         ,
GREATER_EQUAL ,
LESS          ,
LESS_EQUAL    ,
# literals
IDENTIFIER    ,
STRING        ,
NUMBER        ,
# Keywords
AND           ,
CLASS,
ELSE,
FALSE,
FUN,
FOR,
IF,
NIL,
OR,
PRINT,
RETURN,
SUPER,
THIS,
TRUE,
VAR,
WHILE,
# EFO
LOX_EOF
) = (x for x in range(37))


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
        s.append('%s %s %s\n' % (self.token_type, self.literal, self.line))

        return ''.join(s)

    def __repr__(self):
        return self.__str__()
