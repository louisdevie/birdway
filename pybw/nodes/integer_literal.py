from .base import *
from birdway import Type


class IntegerLiteral(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext, Identified):
    def __init__(self):
        super().__init__()
        self.value = int()

    def _type(self):
        return Type.INTEGER

    def _propagate(self, ast, vc, lc, bc):
        return set()

    def _check(self):
        pass

    def _initialise(self):
        return ""

    def _transpile(self, tui):
        return ""

    def _reference(self, tui):
        return str(self.value)
