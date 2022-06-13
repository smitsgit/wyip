from mylexer import Lexer
from parser import Parser


def main():
    while True:
        input_line = input(">>>")
        lexer = Lexer(input_line)
        # for tok in lexer:
        #     print(tok)

        parser = Parser.new(lexer)
        program = parser.parse()
        if parser.errors:
            for msg in parser.errors:
                print(msg)
        else:
            print(program.statements[0].identifier.value)


if __name__ == '__main__':
    main()
