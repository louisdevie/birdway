from .base import *
from birdway import OPERATION_RESULT, Unary


class BinaryOperation(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.operator = None
        self.loperand = None
        self.roperand = None

    def _type(self):
        return OPERATION_RESULT[self.operator][self.loperand.type : self.roperand.type]

    def _initialise(self):
        return self.operand._initialise()

    def _propagate(self, ast, vc, lc, bc):
        self.loperand.context = self.context.copy()
        self.using |= self.loperand._propagate(ast, vc, lc, bc)
        self.roperand.context = self.context.copy()
        self.using |= self.roperand._propagate(ast, vc, lc, bc)
        return self.using

    def _check(self):
        self._type()
        self.loperand._check()
        self.roperand._check()

    # def _transpile(self, tui):
    #     if self.operator == Unary.ISDEF:
    #         return f"{self.operand._transpile(tui+'1')}"
    #     else:
    #         raise TypeError(f"unknown unary operator {self.operator}")

    # def _reference(self, tui):
    #     if self.operator == Unary.ISDEF:
    #         return f"""(*{self.operand._reference(tui+"1")}) != NULL"""
    #     else:
    #         raise TypeError(f"unknown unary operator {self.operator}")
