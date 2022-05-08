from .base import *
from birdway import Category

class ForLoop(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.variable = str()
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

        if (invalid := parser.pop()) != KeywordDo():
            raise BirdwaySyntaxError(
                    f"expected the ‘do’ keyword, got {invalid} at line {invalid._line}"
                )

        loop.result = parser.parse_expression()

        return loop

    def _type(self):
        return self.result.type

    def _propagate(self, ast, vc, lc, bc):
        self.values.context = self.context.copy()
        self.using |= self.values._propagate(ast, vc, lc, bc)
        self.result.context = self.context.copy()
        self.result.context[self.variable] = (vc.register(), self.values.type.val)
        self.using |= self.result._propagate(ast, vc, lc, bc)
        return self.using

    def _check(self):
        check_type(self.values, Category.ITERABLE)
        self.result._check()