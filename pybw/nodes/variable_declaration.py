from .base import *
from birdway import Type


class VariableDeclaration(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext, Identified):
    def __init__(self):
        super().__init__()
        self.name = str()
        self.initial_value = None
        self._t = Type.UNKNOWN

    @classmethod
    def _parse(cls, parser):
        variable = cls()

        match parser.peek(0):
            case Identifier(name=ident):
                parser.eat()
                variable.name = ident

            case other:
                raise BirdwaySyntaxError(
                    f"expected variable name, got {other} at line {other._line}"
                )

        match parser.peek(0):
            case Assignment():
                parser.eat()

            case other:
                raise BirdwaySyntaxError(
                    f"expected ‘=’, got {other} at line {other._line}"
                )

        variable.initial_value = parser.parse_expression()

        return variable

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
        self.result._check()

    def _initialise(self):
        return (
            self.result._initialise()
            + "int "
            + self.id
            + "("
            + ",".join(
                (
                    [ctype(self.result.type) + "*RESULT"]
                    if self.result.type != Type.VOID
                    else []
                )
                + [
                    ctype(self.parameters[p]) + "*param" + str(i)
                    for i, p in enumerate(self.parameters)
                ]
                + [
                    ctype(self.result.context[v][1]) + "*" + self.result.context[v][0]
                    for v in self.result.using
                ]
            )
            + ") {}"
        )

    def _transpile(self, tui):
        return ""
