from abc import ABC, abstractmethod
from dataclasses import dataclass


class Node(ABC):
    @abstractmethod
    def token_literal(self):
        """
        This is typically used for debugging
        """
        ...


class Statement(Node):
    def token_literal(self):
        pass


class Expression(Node):

    def token_literal(self):
        pass


class Identifier(Expression):
    def __init__(self, token: Token, value: Expression):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.literal


class LetStatement(Statement):
    def __init__(self, token: Token, identifier: Identifier, value: Expression):
        self.token = token
        self.identifier = identifier
        self.value = value

    def token_literal(self):
        return self.token.literal


class Program:
    def __init__(self, statements: list[Node] = None):
        if statements is None:
            self.statements = []
        else:
            self.statements = statements

    def token_literal(self):
        if self.statements:
            return self.statements[0].token_literal()
        else:
            return ""
