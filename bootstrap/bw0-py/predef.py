from birdway_types import *


def to_string(value):
    match value.type:
        case Str():
            return value

        case other:
            raise NotImplementedError(f"to_string is not implemented for {other}")
