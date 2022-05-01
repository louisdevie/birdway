from .base import *
from birdway import Type


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

    def _initialise(self):
        return f"""struct BirdwayChar {self.id}[{len(self.string)}] = {{{
            ', '.join([f"{{{ord(char)}, NULL}}" for char in self.string])
            }}};"""

    def _transpile(self, tui):
        return f"""
            struct BirdwayString {tui};
            birdwayStringLiteral(&{tui}, {self.id}, {len(self.string)});"""
