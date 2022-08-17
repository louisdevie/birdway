import sys, pprint

from parser import Parser
from lexer import tokenise
from error import BirdwayError
from interpreter import Interpreter
from signals import ErrorSignal, global_error_message


def main():
    with open(sys.argv[1], "rt", encoding="utf-8") as f:
        source = f.read()

    tokens = tokenise(source)
    try:
        ast = Parser(tokens).parse()

        # pprint.pprint(ast)

        interpreter = Interpreter(ast)
        interpreter.run()
    except BirdwayError as err:
        print("\x1b[31mERROR:", err, "\x1b[0m")
        exit(1)
    except ErrorSignal as sig:
        print(
            "\x1b[31mERROR: uncaught signal",
            type(sig),
            ":",
            global_error_message,
            "\x1b[0m",
        )
        exit(1)


if __name__ == "__main__":
    main()
