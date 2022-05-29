from .base import *


class TryOnThen(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.result = None
        self.handlers = list()
        self.final = None

    @classmethod
    def _parse(cls, parser):
        tryonthen = cls()

        tryonthen.result = parser.parse_expression()

        while parser.peek(0) == KeywordOn():
            parser.eat()
            tryonthen.handlers.append(parser.parse_expression())

        if parser.peek(0) == KeywordThen():
            parser.eat()
            tryonthen.final = parser.parse_expression()

        return tryonthen

    def _type(self):
        return self.statements.type

    def _initialise(self):
        return (
            self.condition._initialise()
            + self.statements._initialise()
            + self.alternative._initialise()
        )

    def _transpile(self, tui):
        return f"""
            {self.condition._transpile(tui+"1")}
            if ({self.condition._reference(tui+"1")})
            {{
                {self.statements._transpile(tui+"2")}
            }}
            else
            {{
                {self.alternative._transpile(tui+"3")}
            }}"""
