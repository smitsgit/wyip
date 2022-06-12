from enum import Enum
from dataclasses import dataclass


class TokenType(Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # identifiers and literals
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"

    # operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    SLASH = "/"
    LT = "<"
    GT = ">"
    BANG = "!"
    NOT_EQUAL = "!="
    EQUAL = "=="

    # Delimiters
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = ")"

    COMMA = ","
    SEMI_COLON = ";"

    # keywords
    LET = "LET"
    FUNCTION = "FUNCTION"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"


@dataclass
class Token:
    type: TokenType
    literal: str
