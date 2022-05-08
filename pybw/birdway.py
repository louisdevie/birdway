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
    FUNCTION = auto()
    VOID = auto()
    BOOLEAN = auto()
    INTEGER = auto()
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
            case Type.INTEGER.value:
                return "int"
            case Type.FUNCTION.value:
                return "func"
            case other:
                raise ValueError(f"unknown type {repr(self)}")


class Composite:
    class Nullable:
        def __init__(self, val):
            self.val = val

        def __str__(self):
            return f"{self.val}?"

    class Table:
        def __init__(self, val, key=None):
            self.val = val
            self.key = key

        def __str__(self):
            return f"[{self.val}]" if self.key is None else f"[{self.key}: {self.val}]"

class _IterableCategory:
    def __eq__(self, t):
        if isinstance(t, Composite.Table):
            return True
        elif t == Type.STRING:
            return True
        else:
            return False

class _GroupCategory:
    def __init__(self, *types):
        self._types = types

    def __eq__(self, t):
        return t in self._types 

class Category:
    ITERABLE = _IterableCategory()
    INDEX = _GroupCategory(Type.INTEGER)

class BaseUserTypePromise:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{type(self)}"


class StructPromise(BaseUserTypePromise):
    pass


class EnumPromise(BaseUserTypePromise):
    pass


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


class _IsdefResult:
    def __getitem__(self, t):
        if t == Type.UNKNOWN:
            return Type.UNKNOWN

        elif isinstance(t, Composite.Nullable):
            return Type.BOOLEAN

        else:
            raise BirdwayTypeError(f"the ? operator can only be used on nullable types")

class _LastResult:
    def __getitem__(self, t):
        if t == Type.UNKNOWN:
            return Type.UNKNOWN

        elif t == Type.STRING:
            return Type.INTEGER

        elif isinstance(t, Composite.Table):
            if t.key != None:
                raise BirdwayTypeError(f"the ## operator can't be used on dictionary tables")

        else:
            raise BirdwayTypeError(f"the ## operator can't be used on {t}")

class _SizeResult:
    def __getitem__(self, t):
        if t == Type.UNKNOWN:
            return Type.UNKNOWN

        elif t == Type.STRING or isinstance(t, Composite.Table):
            return Type.INTEGER

        else:
            raise BirdwayTypeError(f"the ## operator can't be used on {t}")

class _AddResult:
    def __getitem__(self, ts):
        t1, t2 = ts.start, ts.stop

        if t1 == Type.UNKNOWN:
            return Type.UNKNOWN

        elif t1 == Type.INTEGER:
            if t2 == Type.UNKNOWN:
                return Type.UNKNOWN

            elif t2 == Type.INTEGER:
                return Type.INTEGER

        raise BirdwayTypeError(f"the + operator can't be used between {t1} and {t2}")


OPERATION_RESULT = {
    Unary.ISDEF: _IsdefResult(),
    Unary.LAST: _LastResult(),
    Unary.SIZE: _SizeResult(),
    Binary.ADDITION: _AddResult(),
}


class ArgumentModifier(Enum):
    NONE = auto()
    UNIQUE = auto()
    OPTIONAL = auto()
    MULTIPLE = auto()


def _genfeats(*features):
    for i, f in enumerate(features):
        exec(f"global FEATURE_{f}; FEATURE_{f} = {2**i}")


_genfeats(
    "STRING",
    "FORMATTING",
    "PRINTLN",
    "TABLE",
)
