from .base import *
from birdway import Type, Composite


class FunctionDefinition(SyntaxNodeABC, PrettyAutoRepr, Identified):
    def __init__(self):
        self.name = str()

    @classmethod
    def _parse(cls, parser):
        function = cls()

        match parser.peek(0):
            case Identifier(name=ident):
                parser.eat()
                function.name = ident

            case other:
                raise BirdwaySyntaxError(
                    f"expected function name, got {other} at line {other._line}"
                )
