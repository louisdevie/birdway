from birdway_types import *
from operators import Value
from signals import *


def to_string(value):
    match value.type:
        case Str():
            return value

        case other:
            raise NotImplementedError(f"to_string is not implemented for {other}")


def map_file_mode(mode):
    match mode:
        case 1:
            return "rt"


def bw_open(file, mode):
    try:
        f = open(file.internal_object, map_file_mode(mode.internal_object))
        return Value(File(), f)
    except FileNotFoundError:
        global global_error_message
        global_error_message = f"no such file : {file.internal_object}"
        raise NotFoundErrorSignal()


def close(file):
    file.internal_object.close()


def err():
    return Value(Str(), global_error_message)


class PredefConst(Value):
    def __init__(self, *args):
        super().__init__(*args)

    def get(self):
        return self

    def set(self, type, new_val):
        raise BirdwayTypeError("can't set predefined constant")


NAMES = {
    "open": bw_open,
    "READ": PredefConst(Int(), 1),
    "close": close,
    "ERR_ANY": PredefConst(None, ErrorSignal),
    "err": err,
    "FAIL": PredefConst(None, FailSignal),
}
