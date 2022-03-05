import os, sys

import lexer
import parser
import generator


def main():
    count = len(sys.argv) - 1
    for i, target in enumerate(sys.argv[1:]):
        directory, filename = os.path.split(target)
        name, extension = os.path.splitext(filename)

        tempdst = name + ".bwtmp.c"

        print(f"Compiling {target} ... ({i+1}/{count})")

        try:
            with open(target, "rt") as fd:
                content = fd.read()
            tokens = lexer.parse(content)
            for t in tokens:
                print(" ", t)
            ast = parser.parse(tokens)
            print(ast)
            output = generator.transpile(ast)
            with open(tempdst, "wt+") as fd:
                fd.write(output)
        except IOError as err:
            print(f"  Can't open file {target}: {err}")
        except (lexer.BirdwayLexicalError, parser.BirdwaySyntaxError) as err:
            print(f"  Error parsing file {target}: {err}")


if __name__ == "__main__":
    main()
