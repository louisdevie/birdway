import sys, pprint

from parser import Parser
from lexer import tokenise
from error import BirdwayError
from interpreter import Interpreter


def main():
    with open(sys.argv[1], "rt", encoding="utf-8") as f:
        source = f.read()

    tokens = tokenise(source)
    try:
        ast = Parser(tokens).parse()

        interpreter = Interpreter(ast)
        interpreter.run()
    except BirdwayError as err:
        print("\x1b[31mERROR:", err, "\x1b[0m")


if __name__ == "__main__":
    main()
