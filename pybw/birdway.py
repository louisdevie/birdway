from enum import Enum, auto


class Type(Enum):
    UNKNOWN = auto()
    STRING = auto()


class Unary(Enum):
    ISDEF = auto()
