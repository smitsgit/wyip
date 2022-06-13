from mylexer import Lexer
from parser import Parser


def test_parser_let_statement():
    input = """
    let x = 10;
    let y = 55;
    let z = 30;
    """

    lexer = Lexer(input)
    parser = Parser.new(lexer)
    program = parser.parse()
    assert len(parser.errors) == 0
    assert program is not None
    assert len(program.statements) == 3
    assert program.statements[2].identifier.value == "z"


def test_parser_errors_statement():
    input_str = """
    let x 10;
    let 55;
    let z = 30;
    """

    lexer = Lexer(input_str)
    parser = Parser.new(lexer)
    program = parser.parse()
    assert len(parser.errors) == 2


def test_return_statements():
    input = """
        return 10;
        return 55;
        """

    lexer = Lexer(input)
    parser = Parser.new(lexer)
    program = parser.parse()
    assert len(parser.errors) == 0
    assert program is not None
    assert len(program.statements) == 2


def test_identifier_expressions():
    instr = "foobar;"
    lexer = Lexer(instr)
    parser = Parser.new(lexer)
    program = parser.parse()
    assert len(parser.errors) == 0
    assert program is not None
    assert len(program.statements) == 1
    assert str(program) == "foobar"
