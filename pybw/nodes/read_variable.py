from .base import *
from birdway import Type


class ReadVariable(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext, Identified):
    def __init__(self):
        super().__init__()
        self.name = str()
        self._t = Type.UNKNOWN

    def _type(self):
        return self._t

    def _propagate(self, ast, vc, lc, bc):
        if self.name in self.context:
            self.id, self._t = self.context[self.name]
            return {self.name}
        else:
            raise BirdwayNameError(f'no variable/constant named "{self.name}"')

    def _check(self):
        pass

    def _initialise(self):
        return ""

    def _transpile(self, tui):
        return ""

    def _reference(self, tui):
        return self.id
