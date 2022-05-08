from .base import *
from birdway import Type, Composite


class StructDefinition(SyntaxNodeABC, PrettyAutoRepr, Identified):
    def __init__(self):
        super().__init__()
        self.fields = dict()
        self.name = str()

    @classmethod
    def _parse(cls, parser):
        struct = cls()

        match parser.peek(0):
            case Identifier(name=ident):
                parser.eat()
                struct.name = ident

            case other:
                raise BirdwaySyntaxError(
                    f"expected the name of the struct, got {other} at line {other._line}"
                )

        if (invalid := parser.pop()) != OpeningParens():
            raise BirdwaySyntaxError(
                f"expected ‘(’, got {invalid} at line {invalid._line}"
            )

        while parser.remaining():
            t = parser.parse_type()

            match parser.peek(0):
                case Identifier(name=ident):
                    parser.eat()
                    if ident in struct.fields:
                        raise BirdwayNameError(f"duplicate field ‘{name}’")
                    struct.fields[ident] = t

                case other:
                    raise BirdwaySyntaxError(
                        f"expected the name of the struct, got {other} at line {other._line}"
                    )

            if parser.peek(0) == Separator():
                parser.eat()
                if parser.peek(0) == ClosingParens():
                    parser.eat()
                    return struct
            else:
                if parser.peek(0) == ClosingParens():
                    parser.eat()
                    return struct
                else:
                    raise BirdwaySyntaxError(
                        f"expected colon between fields of struct (near line {parser.peek(0)._line})"
                    )

        raise BirdwaySyntaxError("hit EOF while parsing struct definition")
