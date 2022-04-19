from .base import *


class Program(SyntaxNodeABC, PrettyAutoRepr):
    def __init__(self):
        self.metadata = None
        self.arguments = list()
        self.script = None
        self.standard_features = 0
