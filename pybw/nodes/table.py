from .base import *


class Table(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.key_type = Type.UNKNOWN
        self.value_type = Type.UNKNOWN
        self.values = dict()

    def _type(self):
        return Composite.Table(self.value_type, self.key_type)
