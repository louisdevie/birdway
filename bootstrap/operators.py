from error import *
from birdway_types import *
from parser import Node


class Value:
    def __init__(self, type, obj):
        self.type = type
        self.internal_object = obj


def _concat(lhs, rhs, ii):
    lhs = ii.run_dispatch(lhs)
    rhs = ii.run_dispatch(rhs)

    if lhs.type == Str() and rhs.type == Str():
        return Value(Str(), lhs.internal_object + rhs.internal_object)

    raise BirdwayTypeError(f"invalid operands for ‘&&’: {lhs.type} and {rhs.type}")


def _assign(lhs, rhs, ii):
    if lhs["node"] == Node.NAME:
        lhs = ii.resolve(lhs["name"])
        rhs = ii.run_dispatch(rhs)

        lhs.set(rhs.type, rhs.internal_object)

    else:
        raise BirdwayTypeError(f"left operand of assignment isn't a variable")


OP_BIN = {
    "&&": _concat,
    "=": _assign,
}
