from .base import *
from birdway import Type, Composite


class EnumDefinition(SyntaxNodeABC, PrettyAutoRepr, Identified):
    def __init__(self):
        self.values = list()
        self.name = str()

    @classmethod
    def _parse(cls, parser):
        enum = cls()

        match parser.peek(0):
            case Identifier(name=ident):
                parser.eat()
                enum.name = ident

            case other:
                raise BirdwaySyntaxError(
                    f"expected the name of the enum, got {other} at line {other._line}"
                )

        if (invalid := parser.pop()) != OpeningParens():
            raise BirdwaySyntaxError(
                f"expected ‘(’, got {invalid} at line {invalid._line}"
            )

        while parser.remaining():
            match parser.peek(0):
                case Identifier(name=ident):
                    parser.eat()
                    if ident in enum.values:
                        raise BirdwayNameError(f"duplicate value ‘{name}’")
                    enum.values.append(ident)

                case other:
                    raise BirdwaySyntaxError(
                        f"expected the name of the value, got {other} at line {other._line}"
                    )

            if parser.peek(0) == Separator():
                parser.eat()
                if parser.peek(0) == ClosingParens():
                    parser.eat()
                    return enum
            else:
                if parser.peek(0) == ClosingParens():
                    parser.eat()
                    return enum
                else:
                    raise BirdwaySyntaxError(
                        f"expected colon between values of enum (near line {parser.peek(0)._line})"
                    )

        raise BirdwaySyntaxError("hit EOF while parsing enum definition")
