from .base import *


class ForLoop(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.variable = str()
        self.type = Type.UNKNOWN
        self.values = None
        self.result = None

    @classmethod
    def _parse(cls, parser):
        loop = cls()

        match parser.peek(0):
            case Identifier(name=ident):
                parser.eat()
                loop.variable = ident

            case other:
                raise BirdwaySyntaxError(
                    f"expected identifier, got {other} at line {other._line}"
                )

        if (invalid := parser.pop()) != KeywordIn():
            raise BirdwaySyntaxError(
                    f"expected the ‘in’ keyword, got {invalid} at line {invalid._line}"
                )

        loop.values = parser.parse_expression()

        return loop

    def _type(self):
        return self.result.type
