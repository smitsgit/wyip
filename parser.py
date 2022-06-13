from mylexer import Lexer
from tokens import Token, TokenType
from myast import Program, Statement, LetStatement, Identifier, ReturnStatement


class Parser:
    def __init__(self, lexer: Lexer, cur_token: Token = None,
                 peek_token: Token = None):
        self.lexer = lexer
        self.cur_token = cur_token
        self.peek_token = peek_token
        self.errors = []

    def initialize_cur_peek_tokens(self):
        self.next_token()
        self.next_token()

    @classmethod
    def new(cls, lexer: Lexer):
        parser = Parser(lexer)
        parser.initialize_cur_peek_tokens()
        return parser

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse(self) -> Program:
        program = Program()

        while self.cur_token.type != TokenType.EOF:
            statement = self.parse_statement()
            if statement:
                program.statements.append(statement)
            self.next_token()

        return program

    def parse_identifier(self):
        ident = Identifier(self.cur_token, self.cur_token.literal)
        return ident

    def parse_let_statement(self):
        cur_token = self.cur_token
        if not self.peek_token.type == TokenType.IDENTIFIER:
            self.peek_error(TokenType.IDENTIFIER)
            return None

        self.next_token()  # Now cur_token points at identifier
        ident = self.parse_identifier()

        if not self.peek_token.type == TokenType.ASSIGN:
            self.peek_error(TokenType.ASSIGN)
            return None
        self.next_token()  # Now cur_token points at = sign
        self.next_token()  # Now it points to the expression

        while self.cur_token.type != TokenType.SEMI_COLON:
            # At present we don't know how to parse expressions,
            # hence skipping seems a wonderful option :-)
            self.next_token()

        stmt = LetStatement(cur_token, ident, None)
        return stmt

    def parse_return_statement(self):
        cur_token = self.cur_token
        self.next_token()  # Move to the next token

        while self.cur_token.type != TokenType.SEMI_COLON:
            # At present we don't know how to parse expressions,
            # hence skipping seems a wonderful option :-)
            self.next_token()

        stmt = ReturnStatement(cur_token)
        return stmt

    def parse_statement(self) -> Statement:
        match self.cur_token.type:
            case TokenType.LET:
                return self.parse_let_statement()
            case TokenType.RETURN:
                return self.parse_return_statement()

    def peek_error(self, tok_type: TokenType):
        msg = f'expected next token to be of ' \
              f'the {tok_type} but got {self.peek_token.type}'
        self.errors.append(msg)
