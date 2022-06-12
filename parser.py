from mylexer import Lexer
from tokens import Token, TokenType
from myast import Program, Statement, LetStatement, Identifier


class Parser:
    def __init__(self, lexer: Lexer, cur_token: Token = None,
                 peek_token: Token = None):
        self.lexer = lexer
        self.cur_token = cur_token
        self.peek_token = peek_token

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
        if not self.peek_token.type == TokenType.IDENTIFIER:
            return None

        self.next_token()  # Now cur_token points at identifier
        ident = self.parse_identifier()

        if not self.peek_token.type == TokenType.ASSIGN:
            return None
        self.next_token()  # Now cur_token points at = sign
        self.next_token()  # Now it points to the expression

        while self.cur_token.type != TokenType.SEMI_COLON:
            self.next_token()

        stmt = LetStatement(self.cur_token, ident, None)
        return stmt

    def parse_statement(self) -> Statement:
        match self.cur_token.type:
            case TokenType.LET:
                return self.parse_let_statement()
