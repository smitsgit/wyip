class Lexer:
    def __init__(self, input: str):
        self._input = input
        self.position = -1
        self.read_position = self.position + 1
        self.chr = None

    def next_token(self) -> Token:
        self.skip_none()
        self.skip_whitespace()
        tok: TokenType = None
        if self.chr == '=':
            if self.peek_chr() == '=':
                self.read_chr()
                tok = Token(TokenTypes.EQ, "==")
            else:
                tok = Token(TokenTypes.ASSIGN, self.chr)
        elif self.chr == '+':
            tok = Token(TokenTypes.PLUS, self.chr)
        elif self.chr == '-':
            tok = Token(TokenTypes.MINUS, self.chr)
        elif self.chr == '(':
            tok = Token(TokenTypes.LPAREN, self.chr)
        elif self.chr == ')':
            tok = Token(TokenTypes.RPAREN, self.chr)
        elif self.chr == '{':
            tok = Token(TokenTypes.LBRACE, self.chr)
        elif self.chr == '}':
            tok = Token(TokenTypes.RBRACE, self.chr)
        elif self.chr == ',':
            tok = Token(TokenTypes.COMMA, self.chr)
        elif self.chr == ';':
            tok = Token(TokenTypes.SEMICOLON, self.chr)
        elif self.chr == '!':
            if self.peek_chr() == '=':
                self.read_chr()
                tok = Token(TokenTypes.NOT_EQ, "!=")
            else:
                tok = Token(TokenTypes.BANG, self.chr)
        elif self.chr == '*':
            tok = Token(TokenTypes.ASTERISK, self.chr)
        elif self.chr == '/':
            tok = Token(TokenTypes.SLASH, self.chr)
        elif self.chr == '<':
            tok = Token(TokenTypes.LT, self.chr)
        elif self.chr == '>':
            tok = Token(TokenTypes.GT, self.chr)
        elif self.chr == 0:
            tok = Token(TokenTypes.EOF, "")
        else:
            if self.is_letter(self.chr):
                identifier = self.read_identifier()
                if identifier in keywords:
                    return keywords[identifier]
                else:
                    return Token(TokenTypes.IDENT, identifier)
            elif self.is_number(self.chr):
                number = self.read_num()
                return Token(TokenTypes.INT, number)
            else:
                return Token(TokenTypes.ILLEGAL, self.chr)
        self.read_chr()
        return tok

    def read_chr(self):
        if self.read_position < len(self._input) != 0:
            self.chr = self._input[self.read_position]
        else:
            self.chr = 0
        self.position = self.read_position
        self.read_position += 1

    def peek_chr(self) -> str:
        if self.read_position < len(self._input) != 0:
            chr = self._input[self.read_position]
        else:
            chr = 0
        return chr

    def read_identifier(self) -> str:
        position = self.position
        while True:
            if self.is_letter(self.chr):
                self.read_chr()
                continue
            else:
                break

        return self._input[position: self.position]

    def skip_whitespace(self):
        while self.chr in [' ', '\t', '\n', '\r']:
            self.read_chr()

    def is_letter(self, chr: str) -> bool:
        return 'a' <= chr <= 'z' or 'A' <= chr <= 'Z' or chr == '_'

    def is_number(self, chr: str) -> bool:
        return chr.isdigit()

    def read_num(self):
        position = self.position
        while True:
            if self.is_number(self.chr):
                self.read_chr()
                continue
            else:
                break
        return self._input[position: self.position]

    def skip_none(self):
        if self.chr is None:
            self.read_chr()

    def __iter__(self):
        return self

    def __next__(self):
        tok = self.next_token()
        if tok == Token(TokenTypes.EOF, ""):
            raise StopIteration
        return tok
