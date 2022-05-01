from .base import *
from birdway import Type


class PrintLine(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.content = None

    @classmethod
    def _parse(cls, parser):
        println = cls()
        println.content = parser.parse_expression()
        return println

    def _type(self):
        return Type.VOID

    def _initialise(self):
        return self.content._initialise()

    def _transpile(self, tui):
        return f"""
            {self.content._transpile(tui+"1")}
            birdwayPrintln({self.content._reference(tui+"1")});"""
