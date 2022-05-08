from .base import *
from birdway import Type, Category
from exceptions import *


class TableAccess(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext, Identified):
    def __init__(self):
        super().__init__()
        self.table = None
        self.index = None

    def _type(self):
        if self.table.type != Type.UNKNOWN:
            return self.table.type.val

    def _propagate(self, ast, vc, lc, bc):
        self.table.context = self.context.copy()
        self.using |= self.table._propagate(ast, vc, lc, bc)
        self.index.context = self.context.copy()
        self.using |= self.index._propagate(ast, vc, lc, bc)
        return self.using

    def _check(self):
        check_type(self.index, Category.INDEX)
        self.table._check()
