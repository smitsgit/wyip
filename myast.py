from abc import ABC, abstractmethod
from tokens import Token


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


class IntegerLiteral(Expression):
    def __init__(self, token: Token, value: int):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return str(self.value)


class Identifier(Expression):
    def __init__(self, token: Token, value: Expression):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return str(self.value)


class LetStatement(Statement):
    def __init__(self, token: Token, identifier: Identifier, value: Expression):
        self.token = token
        self.identifier = identifier
        self.value = value

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return " ".join([self.token.literal, self.identifier.value,
                         TokenType.ASSIGN, str(self.value), ";"])


class ReturnStatement(Statement):
    def __init__(self, token: Token, return_val: Expression = None):
        self.token = token
        self.return_val = return_val

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return " ".join([self.token.literal, str(self.return_val), ";"])


class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Expression = None):
        self.token = token
        self.expression = expression

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        if self.expression is not None:
            return " ".join([str(self.expression)])
        else:
            return ""


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

    def __str__(self):
        return " ".join([str(stmt) for stmt in self.statements])
