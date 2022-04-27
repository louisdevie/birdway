from enum import Enum, auto
from exceptions import *


class Typed:
    def __getattr__(self, attr):
        if attr == "type":
            return self._type()
        else:
            return super().__getattr__(attr)

    def _type(self):
        raise NotImplementedError()


class Type(Enum):
    UNKNOWN = auto()
    VOID = auto()
    BOOLEAN = auto()
    STRING = auto()

    def __str__(self):
        match self.value:
            case Type.UNKNOWN.value:
                return "~"
            case Type.STRING.value:
                return "str"
            case Type.VOID.value:
                return "void"
            case Type.BOOLEAN.value:
                return "bool"
            case other:
                raise ValueError(f"unknown type")


class Composite:
    class Nullable:
        def __init__(self, val):
            self.val = val

        def __repr__(self):
            return f"{self.val}?"

    class Table:
        def __init__(self, val, key=None):
            self.val = val
            self.key = key

        def __repr__(self):
            return f"[{self.val}]" if self.key is None else f"[{self.key}: {self.val}]"


class Unary(Enum):
    ISDEF = auto()
    ISNTDEF = auto()
    LAST = auto()
    SIZE = auto()
    INVERSE = auto()
    OPPOSITE = auto()
    BITWISENOT = auto()
    LOGICALNOT = auto()


class Binary(Enum):
    ADDITION = auto()
    SUBSTRACTION = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
    MODULO = auto()
    INTDIVISON = auto()
    BITWISEAND = auto()
    BITWISEOR = auto()
    BITWISEXOR = auto()
    BITSHIFTL = auto()
    BITSHIFTR = auto()
    LOGICALAND = auto()
    LOGICALOR = auto()
    LOGICALXOR = auto()
    CONCATENATION = auto()


def isdef_result(t):
    if t == Type.UNKNOWN:
        return Type.UNKNOWN

    elif isinstance(t, Composite.Nullable):
        return Type.BOOLEAN

    else:
        raise BirdwayTypeError(f"the ? operator can only be used on nullable types")


OPERATION_RESULT = {
    Unary.ISDEF: isdef_result,
}


class ArgumentModifier(Enum):
    NONE = auto()
    UNIQUE = auto()
    OPTIONAL = auto()
    VARIADIC = auto()


def _genfeats(*features):
    for i, f in enumerate(features):
        exec(f"global FEATURE_{f}; FEATURE_{f} = {2**i}")


_genfeats(
    "STRING",
    "FORMATTING",
    "PRINTLN",
)
