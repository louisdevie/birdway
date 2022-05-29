from abc import ABC
from birdway import Typed, Type, Composite
from autorepr import PrettyAutoRepr
from tokens import *
from exceptions import *

SUCCESS = 0


class SyntaxNodeABC(ABC):
    def _propagate(self, ast, vc, lc, bc):
        raise TypeError(f"can't resolve variables for node of type {type(self)}")

    def _check(self):
        raise TypeError(f"can't check node of type {type(self)}")

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


def nameof(T):
    match T:
        case Type.STRING:
            return "Str"

        case Type.INTEGER:
            return "Int"

        case Composite.Nullable(val=val):
            return "Nullable" + nameof(val)

        case other:
            raise TypeError(f"no type name for <{other}>")


def ctype(T):
    match T:
        case Type.VOID:
            return "void "

        case Type.STRING:
            return "struct BirdwayString "

        case Type.INTEGER:
            return "int32_t "

        case Composite.Nullable(val=val):
            return ctype(val) + "*"

        case Composite.Table(val=val, key=None):
            return f"struct BirdwayListTable{nameof(val)} "

        case other:
            raise TypeError(f"no equivalent C type for <{other}>")


def check_type(node, expected):
    node._check()
    if node.type != expected:
        raise BirdwayTypeError(f"expected type <{expected}>, got <{node.type}>")
