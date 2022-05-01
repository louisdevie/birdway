from .base import *


class IfThenElse(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.condition = None
        self.statements = None
        self.alternative = None

    @classmethod
    def _parse(cls, parser):
        ifthenelse = cls()

        ifthenelse.condition = parser.parse_expression()

        if (tok := parser.pop()) != KeywordThen():
            raise BirdwaySyntaxError(
                f"expected keyword then, got {tok} on line {tok._line}"
            )

        ifthenelse.statements = parser.parse_expression()

        if parser.peek(0) == KeywordElse():
            parser.eat()
            ifthenelse.alternative = parser.parse_expression()

        return ifthenelse

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
