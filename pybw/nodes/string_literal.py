from .base import *
from birdway import Type, FEATURE_STRING


class StringLiteral(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext, Identified):
    def __init__(self):
        super().__init__()
        self.string = str()

    @classmethod
    def _parse(cls, parser):
        string = cls()

        while parser.remaining():
            match parser.peek(0):
                case StringDelimiter():
                    parser.eat()
                    if parser.peek(0) == StringDelimiter():
                        parser.eat()
                    else:
                        return string

                case StringContent(value=val):
                    parser.eat()
                    string.string += val

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing string"
                    )

        raise BirdwaySyntaxError("hit EOF while parsing string")

    def _type(self):
        return Type.STRING

    def _propagate(self, ast, vc, lc, bc):
        ast.standard_features |= FEATURE_STRING
        self.id = f"STRING_LITERAL_{lc.register()}"
        return set()

    def _check(self):
        pass

    def _initialise(self):
        return f"""struct BirdwayChar {self.id}[{len(self.string)}] = {{{
            ', '.join([f"{{{ord(char)}, NULL}}" for char in self.string])
            }}};"""

    def _transpile(self, tui):
        return f"""
            struct BirdwayString {tui};
            birdwayStringLiteral(&{tui}, {self.id}, {len(self.string)});"""
