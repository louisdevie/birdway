from .base import *
from birdway import Type, Composite


class FunctionDefinition(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext, Identified):
    def __init__(self):
        super().__init__()
        self.name = str()
        self.parameters = list()
        self.result = None

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

        match parser.peek(0):
            case OpeningParens():
                parser.eat()

            case other:
                return function

        while parser.remaining():
            match parser.peek(0):
                case Identifier(name=ident):
                    parser.eat()
                    function.parameters.append(ident)

                case other:
                    raise BirdwaySyntaxError(
                        f"expected function parameter name, got {other} at line {other._line}"
                    )

            if parser.peek(0) == Separator():
                parser.eat()
                if parser.peek(0) == ClosingParens():
                    parser.eat()
                    break
            else:
                if parser.peek(0) == ClosingParens():
                    parser.eat()
                    break
                else:
                    raise BirdwaySyntaxError(
                        f"expected colon between function parameters (line {parser.peek(0)._line})"
                    )
        else:
            raise BirdwaySyntaxError("hit EOF while parsing function parameters")

        if (invalid := parser.pop()) != Return():
            raise BirdwaySyntaxError(f"expected ‘->’, got {invalid} at line {invalid._line}")

        function.result = parser.parse_expression()

        return function

    def _type(self):
        return Type.VOID

    def _propagate(self, ast, vc, lc, bc):
        if self.result is not None:
            self.result.context = self.context.copy()
            self.using |= self.result._propagate(ast, vc, lc, bc)
            return self.using
        else:
            return set()

    def _check(self):
        pass