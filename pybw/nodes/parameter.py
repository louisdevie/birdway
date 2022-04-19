from .base import *
from birdway import Type, ArgumentModifier, Composite


class Parameter(SyntaxNodeABC, PrettyAutoRepr, Identified):
    def __init__(self):
        self.type = Type.UNKNOWN
        self.modifier = ArgumentModifier.NONE
        self.name = str()
        self.description = str()

    def _initialise(self):
        if self.modifier == ArgumentModifier.OPTIONAL:
            T = Composite.Nullable(self.type)
            init = "= NULL"
        else:
            raise NotImplementedError()
        return f"{ctype(T)} {self.id} {init};\n"
