from .base import *
from birdway import Type
from exceptions import *
from .function_definition import FunctionDefinition


class Block(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext, Identified):
    def __init__(self):
        super().__init__()
        self.statements = list()

    @classmethod
    def _parse(cls, parser):
        block = cls()

        while parser.remaining():
            match parser.peek(0):
                case BlockEnd():
                    parser.eat()
                    return block

                case _:
                    block.statements.append(parser.parse_expression())
                    if parser.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(
                            f"missing semicolon on line {parser.peek(0)._line}"
                        )
                    parser.eat()

        raise BirdwaySyntaxError("hit EOF while parsing block")

    def _type(self):
        return Type.VOID

    def _propagate(self, ast, vc, lc, bc):
        self.id = f"block_{bc.register()}"
        for child in self.statements:
            if isinstance(child, FunctionDefinition):
                child.id = f"func_{vc.register()}"
                self.context[child.name] = (child.id, Type.FUNCTION)
            child.context = self.context.copy()
            self.using |= child._propagate(ast, vc, lc, bc)
        return self.using

    def _check(self):
        for child in self.statements:
            check_type(child, Type.VOID)

    def _initialise(self):
        return f"""
            {"".join([s._initialise() for s in self.statements])}
            int {self.id}({
                "".join(
                    [
                        ctype(self.context[v][1]) + "*" + self.context[v][0]
                        for v in self.using
                    ]
                )
            }) {{
                int err = {SUCCESS};
                {"".join([
                    s._transpile("tmp"+str(i))
                    for i, s in enumerate(self.statements)
                ])}
                return err;
            }}"""

    def _transpile(self, tui):
        return (
            f"err = {self.id}({''.join([self.context[v][0] for v in self.using])});"
            "if (err) {return err;}"
        )
