from abc import ABC
from birdway import Typed, Type, Composite
from autorepr import PrettyAutoRepr

SUCCESS = 0


class SyntaxNodeABC(ABC):
    pass

    def _initialise(self):
        raise TypeError(f"can't initialise node of type {type(self)}")

    def _transpile(self, tui):
        raise TypeError(f"no implementation for node of type {type(self)}")

    def _reference(self, tui):
        return "&" + tui


class InContext:
    def __init__(self):
        self.context = dict()
        self.using = set()


class Identified:
    def __init__(self):
        self.id = str()


def ctype(T):
    match T:
        case Type.STRING:
            return "struct BirdwayString "

        case Composite.Nullable(val=val):
            return ctype(val)+"*"

        case other:
            raise TypeError(f"no internal type for <{other}>")