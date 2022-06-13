from mylexer import Lexer
from tokens import Token, TokenType
from myast import Program, Statement, \
    LetStatement, Identifier, ReturnStatement, ExpressionStatement, Expression
from enum import IntEnum
from typing import Callable


class Precedence(IntEnum):
    LOWEST = 1,
    EQUALS = 2,
    LESS_GREATER = 3,
    SUM = 4,  # + -
    PRODUCT = 5,  # * /
    PREFIX = 6,
    CALL = 7


class Parser:
    def __init__(self, lexer: Lexer, cur_token: Token = None,
                 peek_token: Token = None):
        self.lexer = lexer
        self.cur_token = cur_token
        self.peek_token = peek_token
        self.errors = []
        self.prefix_parsers: Dict[Token, Callable[[], Expression]] = {}
        self.infix_parsers: Dict[Token, Callable[[Expression], Expression]] = {}

    def register_prefix(self, token: TokenType, func: Callable[[], Expression]):
        self.prefix_parsers[token] = func

    def register_infix(self, token: TokenType, func: Callable[[Expression], Expression]):
        self.infix_parsers[token] = func

    def initialize_cur_peek_tokens(self):
        self.next_token()
        self.next_token()

    @classmethod
    def new(cls, lexer: Lexer):
        parser = Parser(lexer)
        parser.initialize_cur_peek_tokens()
        parser.register_prefix(TokenType.IDENTIFIER, parser.parse_identifier)
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

    def parse_expression(self, priority):
        prefix_fn = self.prefix_parsers[self.cur_token.type]
        if prefix_fn is None:
            print(f"No prefix parser found for {self.cur_token.type}")
            return None
        left_exp = prefix_fn()
        return left_exp

    def parse_expression_statement(self):
        cur_token = self.cur_token
        expression = self.parse_expression(Precedence.LOWEST)

        stmt = ExpressionStatement(cur_token, expression)
        if self.peek_token.type == TokenType.SEMI_COLON:
            self.next_token()
        return stmt

    def parse_statement(self) -> Statement:
        match self.cur_token.type:
            case TokenType.LET:
                return self.parse_let_statement()
            case TokenType.RETURN:
                return self.parse_return_statement()
            case _:
                return self.parse_expression_statement()

    def peek_error(self, tok_type: TokenType):
        msg = f'expected next token to be of ' \
              f'the {tok_type} but got {self.peek_token.type}'
        self.errors.append(msg)
