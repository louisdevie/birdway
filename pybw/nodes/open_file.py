from .base import *


class OpenFile(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.path = str()
        self.mode = None
        self.name = str()

    @classmethod
    def _parse(cls, parser):
        openfile = cls()

        openfile.path = parser.parse_expression()

        if (invalid := parser.pop()) != KeywordMode():
            raise BirdwaySyntaxError(
                f"expected keyword ‘mode’, got {invalid} on line {invalid._line}"
            )

        openfile.mode = parser.parse_expression()

        if (invalid := parser.pop()) != KeywordAs():
            raise BirdwaySyntaxError(
                f"expected keyword ‘as’, got {invalid} on line {invalid._line}"
            )

        openfile.mode = parser.parse_expression()

        return openfile

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
