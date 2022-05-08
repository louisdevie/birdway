from .base import *
from birdway import Type, Composite


class FunctionCall(SyntaxNodeABC, PrettyAutoRepr, Identified, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.name = str()
        self.arguments = list()

    def _type(self):
        return Type.VOID

    def _propagate(self, ast, vc, lc, bc):
        if self.name in self.context:
            self.id, t = self.context[self.name]
            if t != Type.FUNCTION:
                raise BirdwayTypeError(f"{self.name} is not a function")
            for arg in self.arguments:
                arg.context = self.context.copy()
                arg._propagate(ast, vc, lc, bc)
            return {self.name}
        else:
            raise BirdwayNameError(f'no function named "{self.name}"')

    def _check(self):
        for child in self.arguments:
            child._check()
