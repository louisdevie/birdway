from error import *
from birdway_types import *


class Value:
    def __init__(self, type, obj):
        self.type = type
        self.internal_object = obj


def _concat(lhs, rhs):
    if lhs.type == Str() and rhs.type == Str():
        return Value(Str(), lhs.internal_object + rhs.internal_object)

    raise BirdwayTypeError(f"invalid operands for ‘&&’: {lhs.type} and {rhs.type}")


OP_BIN = {
    "&&": _concat,
}
