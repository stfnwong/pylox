"""
SCANNER
Token Scanner class

Stefan Wong 2018
"""

from typing import Any, Dict, List, Union
from loxpy import Token

# Debug
#from pudb import set_trace; set_trace()

class Scanner:
    def __init__(self, source:str, verbose:bool=False) -> None:
        if type(source) is not str:
            raise ValueError('source must be a string')

        self.source      :str  = source
        self.token_list  :list = []
        # Source position
        self.src_start   :int  = 0
        self.src_current :int  = 0
        self.src_line    :int  = 1
        # reserved words
        self.reserved_words : Dict[str, int] = {
            "and"    : Token.AND,
            "class"  : Token.CLASS,
            "else"   : Token.ELSE,
            "false"  : Token.FALSE,
            "for"    : Token.FOR,
            "fun"    : Token.FUN,
            "if"     : Token.IF,
            "nil"    : Token.NIL,
            "or"     : Token.OR,
            "print"  : Token.PRINT,
            "return" : Token.RETURN,
            "super"  : Token.SUPER,
            "this"   : Token.THIS,
            "true"   : Token.TRUE,
            "var"    : Token.VAR,
            "while"  : Token.WHILE
        }
        # debug mode
        self.verbose:bool = verbose

    def __str__(self) -> str:
        s = []
        s.append('Lox Scanner\n')
        s.append('source length : %d\n' % len(self.source))
        return ''.join(s)

    def __repr__(self) -> str:
        s = []
        s.append('Scanner [start : %d\t current: %d\t line: %d]' % (self.src_start, self.src_current, self.src_line))
        return ''.join(s)

    # Internal lexing functions
    def _src_end(self) -> bool:
        return self.src_current >= len(self.source)

    def _advance(self) -> str:
        self.src_current += 1
        return self.source[self.src_current-1]

    def _identifier(self) -> None:
        while self._isalphanumeric(self._peek()):
            self._advance()

        text = self.source[self.src_start:self.src_current]
        if text in self.reserved_words.keys():
            token_type = self.reserved_words[text]
        else:
            token_type = Token.IDENTIFIER
        self._add_token(token_type)

    def _isalpha(self, c:str) -> bool:
        if ord(c) in range(65,91) or ord(c) in range(97, 123):
            return True
        return False

    def _isalphanumeric(self, c:str) -> bool:
        if self._isalpha(c) or self._isdigit(c):
            return True
        return False

    def _isdigit(self, c:str) -> bool:
        # While we could use str.isdigit() here, this function allows us
        # to write self._isdigit(self._peek()) and consume the output
        # of self._peek() in a loop
        if ord(c) in range(48, 58):
            return True

        return False

    def _match(self, expected_char:str) -> bool:
        """
        Only consume input if this is the character we expect
        """
        if self._src_end():
            return False
        if self.source[self.src_current] != expected_char:
            return False
        self.src_current += 1

        return True

    def _number(self) -> None:
        while self._isdigit(self._peek()) is True:
            self._advance()

        # Check for fractional part
        if self._peek() == '.' and self._isdigit(self._peek_next()):
            self._advance()
            while(self._isdigit(self._peek())):
                self._advance()

        # Now add a new number token
        self._add_token(Token.NUMBER,
                float(self.source[self.src_start:self.src_current]))

    def _peek(self) -> str:
        if self._src_end():
            return '\0'
        return self.source[self.src_current]

    def _peek_next(self) -> str:
        if self._src_end() or (self.src_current + 1) > len(self.source):
            return '\0'
        return self.source[self.src_current + 1]

    def _parse_string(self) -> None:
        while self._peek() != '"' and self._src_end() is not False:
            if self._peek() == '\n':
                self.src_line += 1
            self._advance()

        # Handle unterminated string
        if self._src_end():
            print('line %d: unterminated string\n' % (self.src_line))
            return

        # Closing quote
        self._advance()
        # trim surrounding quotes
        value = self.source[self.src_start + 1 : self.src_current - 1]
        self._add_token(Token.STRING, value)

    def _add_token(self, token_type:int, literal:Any=None) -> None:
        if literal is None:
            text = ''
        else:
            text = self.source[self.src_start : self.src_current]
        token = Token.Token(token_type, text, literal, self.src_line)
        self.token_list.append(token)

    def _scan_token(self) -> None:
        """
        Scan a single token from the source
        """
        c = self._advance()
        # single character tokens
        if c == '(':
            self._add_token(Token.LEFT_PAREN)
        elif c == ')':
            self._add_token(Token.RIGHT_PAREN)
        elif c == '{':
            self._add_token(Token.LEFT_BRACE)
        elif c == '}':
            self._add_token(Token.RIGHT_BRACE)
        elif c == ',':
            self._add_token(Token.COMMA)
        elif c == '.':
            self._add_token(Token.DOT)
        elif c == '-':
            self._add_token(Token.MINUS)
        elif c == '+':
            self._add_token(Token.PLUS)
        elif c == ';':
            self._add_token(Token.SEMICOLON)
        elif c == '*':
            self._add_token(Token.STAR)
        # Two character tokens
        elif c == '!':
            if self._match('='):
                self._add_token(Token.BANG_EQUAL)
            else:
                self._add_token(Token.BANG)
        elif c == '=':
            if self._match('='):
                self._add_token(Token.EQUAL_EQUAL)
            else:
                self._add_token(Token.EQUAL)
        elif c == '<':
            if self._match('='):
                self._add_token(Token.LESS_EQUAL)
            else:
                self._add_token(Token.LESS)
        elif c == '>':
            if self._match('='):
                self._add_token(Token.GREATER_EQUAL)
            else:
                self._add_token(Token.GREATER)
        # Because comments in Lox begin with a slash, we need
        # some extra logic here
        elif c == '/':
            if self._match('/'):
                # Comment - runs until end of line
                while(self._peek() != '\n' and self._src_end() == False):
                    self._advance()
            else:
                self._add_token(Token.SLASH)
        # String literals
        elif c == '"':
            self._parse_string()
        # Consume whitespace
        elif c == ' ' or c == '\r' or c == '\t':
            pass
        elif c == '\n':
            self.src_line += 1
        else:
            #if c.isdigit():
            if self._isdigit(c):
                self._number()
            elif self._isalpha(c):
                self._identifier()
            else:
                print("line %d: unexpected character %s" % (self.src_line, c))

        if self.verbose:
            print('%s' % self.__repr__())

    def scan(self) -> List[Token.Token]:
        """
        Scan across the entire source and produce a list of all tokens
        """
        self.src_current = 0
        self.src_start = 0
        while(self._src_end() == False):
            self.src_start = self.src_current
            self._scan_token()

        token = Token.Token(Token.LOX_EOF, "", None, self.src_line)
        self.token_list.append(token)

        return self.token_list
