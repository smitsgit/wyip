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
    assert len(program.statements) == 1
