from lexer import Lexer


def main():
    while True:
        input_line = input(">>>")
        lexer = Lexer(input_line)
        for tok in lexer:
            print(tok)


if __name__ == '__main__':
    main()
