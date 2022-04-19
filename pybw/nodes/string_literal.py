from .base import *
from birdway import Type


class StringLiteral(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext, Identified):
    def __init__(self):
        super().__init__()
        self.string = str()

    def _type(self):
        return Type.STRING

    def _initialise(self):
        return f"""struct BirdwayChar {self.id}[{len(self.string)}] = {{{
            ', '.join([f"{{{ord(char)}, NULL}}" for char in self.string])
            }}};"""

    def _transpile(self, tui):
        return f"""
            struct BirdwayString {tui};
            birdwayStringLiteral(&{tui}, {self.id}, {len(self.string)});"""
