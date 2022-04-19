from .base import *
from birdway import Type


class ReadVariable(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext, Identified):
    def __init__(self):
        super().__init__()
        self.name = str()
        self._t = Type.UNKNOWN

    def _type(self):
        return self._t

    def _initialise(self):
        return ""

    def _transpile(self, tui):
        return ""

    def _reference(self, tui):
        return self.id
