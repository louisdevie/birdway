from .base import *


class IfThenElse(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.condition = None
        self.statements = None
        self.alternative = None

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
