import os
from pathlib import Path


def same(iterable):
    if len(iterable) != 0:
        ref = iterable[0]
        for val in iterable:
            if val != ref:
                return False
    return True


def find_module(name, parent_path):
    p = Path(parent_path).parent
    for f in os.listdir(p):
        if f == name + ".bw":
            return p / f
