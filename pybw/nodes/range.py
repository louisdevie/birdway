from .base import *
from birdway import Type
from exceptions import *


class Range(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext, Identified):
    def __init__(self):
        super().__init__()
        self.start = None
        self.end = None
        self.step = None

    def _type(self):
        return self.start.type

    def _propagate(self, ast, vc, lc, bc):
        self.start.context = self.context.copy()
        self.using |= self.start._propagate(ast, vc, lc, bc)
        self.end.context = self.context.copy()
        self.using |= self.end._propagate(ast, vc, lc, bc)
        if self.step is not None:
            self.step.context = self.context.copy()
            self.using |= self.step._propagate(ast, vc, lc, bc)
        return self.using

    def _check(self):
        pass

    def _initialise(self):
        return (
            self.start._initialise()
            + self.end._initialise()
            + (self.step._initialise() if self.step is not None else "")
        )

    def _transpile(self, tui):
        return (
            self.start._transpile(tui + "1")
            + self.end._transpile(tui + "2")
            + (self.step._transpile(tui + "3") if self.step is not None else "")
        )
