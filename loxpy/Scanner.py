"""
SCANNER
Token Scanner class

Stefan Wong 2018
"""

from loxpy import Token

class Scanner(object):
    def __init__(self, source):
        if type(source) is not str:     # TODO : actually, this should be a list of strings
            raise ValueError('source must be a string')

        self.source = source
        self.token_list = []
        # Source position
        self.src_start = 0
        self.src_current = 0
        self.src_line = 1

    def _src_end(self):
        return self.src_current >= len(self.source)

    def _advance(self):
        self.src_current += 1
        return self.source[self.src_current-1]

    def _isdigit(self, c):
        # While we could use str.isdigit() here, this function allows us
        # to write self._isdigit(self._peek()) and consume the output
        # of self._peek() in a loop
        if c >= '0' and c <= '9':
            return True

        return False

    def _match(self, expected_char):
        """
        Only consume input if this is the character we expect
        """
        if self._src_end():
            return False
        if self.source[self.src_current] != expected_char:
            return False
        self.src_current += 1

        return True

    def _number(self):
        while self._isdigit(self._peek) is True:
            self._advance()

        # Check for fractional part
        if self._peek() == '.' and self._isdigit(self._peek_next()):
            self._advance()
            while(self._isdigit(self._peek())):
                self._advance()

        # Now add a new number token
        self._add_token(Token.NUMBER,
                        float(self.source[self.src_start:self.src_current]))

    def _peek(self):
        if self._src_end():
            return '\0'
        return self.source[self.src_current]

    def _peek_next(self):
        if self._src_end() or (self.src_current + 1) > len(self.source):
            return '\0'
        return self.source[self.src_current + 1]

    def _parse_string(self):
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

    def _add_token(self, token_type, literal=None):

        if literal is None:
            text = ''
        else:
            text = self.source[self.src_start : self.src_current]
        token = Token.Token(token_type, text, literal, self.src_current)
        self.token_list.append(token)


    def _scan_token(self):
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
            break
        elif c == '\n':
            self.src_line += 1
        else:
            if c.isdigit():
                self._number()
            else:
                print("line %d: unexpected character %s" % (self.src_line, c))


    def scan(self):
        """
        Scan across the entire source and produce a list of all tokens
        """
        while(self._src_end() == False):
            self.src_start = self.src_current
            self._scan_token()

        token = Token.Token(Token.LOX_EOF, "", None, self.src_line)
        self.token_list.append(token)
