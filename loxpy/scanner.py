"""
SCANNER
Token Scanner class

"""

from typing import Any, Dict, List
from loxpy.token import Token, TokenType


class Scanner:
    def __init__(self, source: str, verbose: bool=False) -> None:
        if type(source) is not str:
            raise ValueError('source must be a string')

        self.source      :str  = source
        self.token_list  :List[Token] = []

        # Source position
        self.src_start   :int  = 0
        self.src_current :int  = 0
        self.src_line    :int  = 1
        self.cur_col     :int  = 1

        # reserved words
        self.reserved_words : Dict[str, TokenType] = {
            "and"    : TokenType.AND,
            "class"  : TokenType.CLASS,
            "else"   : TokenType.ELSE,
            "false"  : TokenType.FALSE,
            "for"    : TokenType.FOR,
            "func"   : TokenType.FUNC,
            "if"     : TokenType.IF,
            "nil"    : TokenType.NIL,
            "or"     : TokenType.OR,
            "print"  : TokenType.PRINT,
            "return" : TokenType.RETURN,
            "super"  : TokenType.SUPER,
            "this"   : TokenType.THIS,
            "true"   : TokenType.TRUE,
            "var"    : TokenType.VAR,
            "while"  : TokenType.WHILE
        }
        # debug mode
        self.verbose: bool = verbose

    def __repr__(self) -> str:
        return f"Scanner [start : {self.src_start}\t current: {self.src_current}\t line: {self.src_line}]"

    # Internal lexing functions
    def _src_end(self) -> bool:
        return self.src_current >= len(self.source)

    def _advance(self) -> str:
        self.src_current += 1
        self.cur_col += 1
        return self.source[self.src_current-1]

    def _new_line(self) -> None:
        self.src_line += 1
        self.cur_col = 1

    def _identifier(self) -> None:
        while self._isalphanumeric(self._peek()):
            self._advance()

        text = self.source[self.src_start:self.src_current]
        if text in self.reserved_words.keys():
            token_type = self.reserved_words[text]
        else:
            token_type = TokenType.IDENTIFIER
        self._add_token(token_type, text)

    def _isalpha(self, c:str) -> bool:
        # '_' is ASCII 95
        if ord(c) in range(65,91) or ord(c) in range(97, 123) or ord(c) == 95:
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
        self._add_token(
            TokenType.NUMBER,
            float(self.source[self.src_start:self.src_current])
        )

    def _peek(self) -> str:
        if self._src_end():
            return '\0'
        return self.source[self.src_current]

    def _peek_next(self) -> str:
        if self._src_end() or (self.src_current + 1) > len(self.source):
            return '\0'
        return self.source[self.src_current + 1]

    def _parse_string(self) -> None:
        while self._peek() != '"' and self._src_end() is False:
            if self._peek() == '\n':
                self._new_line()
            self._advance()

        # Handle unterminated string
        if self._src_end():
            print(f"line {self.src_line}: unterminated string")
            return

        # Consume closing quote
        self._advance()
        # trim surrounding quotes
        value = self.source[self.src_start + 1 : self.src_current - 1]
        self._add_token(TokenType.STRING, value)

    def _add_token(self, token_type: TokenType, literal:Any=None) -> None:
        text = self.source[self.src_start : self.src_current]
        token = Token(token_type, text, literal, self.src_line, self.cur_col)
        self.token_list.append(token)

    def _scan_token(self) -> None:
        """
        Scan a single token from the source
        """
        c = self._advance()
        # single character tokens
        if c == '(':
            self._add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self._add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self._add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self._add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self._add_token(TokenType.COMMA)
        elif c == '.':
            self._add_token(TokenType.DOT)
        elif c == '-':
            self._add_token(TokenType.MINUS)
        elif c == '+':
            self._add_token(TokenType.PLUS)
        elif c == ';':
            self._add_token(TokenType.SEMICOLON)
        elif c == '*':
            self._add_token(TokenType.STAR)
        # Two character tokens
        elif c == '!':
            if self._match('='):
                self._add_token(TokenType.BANG_EQUAL)
            else:
                self._add_token(TokenType.BANG)
        elif c == '=':
            if self._match('='):
                self._add_token(TokenType.EQUAL_EQUAL)
            else:
                self._add_token(TokenType.EQUAL)
        elif c == '<':
            if self._match('='):
                self._add_token(TokenType.LESS_EQUAL)
            else:
                self._add_token(TokenType.LESS)
        elif c == '>':
            if self._match('='):
                self._add_token(TokenType.GREATER_EQUAL)
            else:
                self._add_token(TokenType.GREATER)
        # Because comments in Lox begin with a slash, we need
        # some extra logic here
        elif c == '/':
            if self._match('/'):
                # Comment - runs until end of line
                while(self._peek() != '\n' and self._src_end() == False):
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        # String literals
        elif c == '"':
            self._parse_string()
        # Consume whitespace
        elif c == ' ' or c == '\r' or c == '\t':
            pass
        elif c == '\n':
            self._new_line()
        else:
            if self._isdigit(c):
                self._number()
            elif self._isalpha(c):
                self._identifier()
            else:
                print(f"line {self.src_line}: unexpected character {c}")

        if self.verbose:
            print('%s' % self.__repr__())

    def scan(self) -> List[Token]:
        """
        Scan across the entire source and produce a list of all tokens
        """
        self.src_current = 0
        self.src_start = 0
        while(self._src_end() == False):
            self.src_start = self.src_current
            self._scan_token()

        token = Token(TokenType.LOX_EOF, "", None, self.src_line)
        self.token_list.append(token)

        return self.token_list
