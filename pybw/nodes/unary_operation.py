from .base import *
from birdway import OPERATION_RESULT, Unary


class UnaryOperation(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.operator = None
        self.operand = None

    def _type(self):
        return OPERATION_RESULT[self.operator][self.operand.type]

    def _propagate(self, ast, vc, lc, bc):
        self.operand.context = self.context.copy()
        self.using |= self.operand._propagate(ast, vc, lc, bc)
        return self.using

    def _check(self):
        self._type()
        self.operand._check()

    def _initialise(self):
        return self.operand._initialise()

    def _transpile(self, tui):
        if self.operator in [Unary.ISDEF, Unary.SIZE, Unary.LAST]:
            return self.operand._transpile(tui + "1")
        else:
            raise TypeError(f"unknown unary operator {self.operator}")

    def _reference(self, tui):
        if self.operator == Unary.ISDEF:
            return f"""({self.operand._reference(tui+"1")}) != NULL"""
        if self.operator == Unary.SIZE:
            return f"""({self.operand._reference(tui+"1")}).size"""
        if self.operator == Unary.LAST:
            return f"""({self.operand._reference(tui+"1")}).size - 1"""
        else:
            raise TypeError(f"unknown unary operator {self.operator}")
