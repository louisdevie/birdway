from .base import *

from .parameter import Parameter
from .block import Block
from .option import Option
from .struct_definition import StructDefinition
from .enum_definition import EnumDefinition


class Program(SyntaxNodeABC, PrettyAutoRepr):
    def __init__(self):
        super().__init__()
        self.metadata = None
        self.parameters = list()
        self.flags_and_options = list()
        self.script = None
        self.user_types = list()
        self.standard_features = 0
        self.table_list_types = list()

    @classmethod
    def _parse(cls, parser):
        prog = cls()

        while parser.remaining():
            match parser.peek(0):
                case KeywordMeta():
                    parser.eat()
                    prog.metadata = parser.parse_expression()

                case KeywordParam():
                    parser.eat()
                    prog.parameters.append(Parameter._parse(parser))

                case KeywordRun():
                    parser.eat()
                    if parser.peek(0) == BlockBegin():
                        parser.eat()
                        prog.script = Block._parse(parser)
                    else:
                        prog.script = parser.parse_expression()

                case KeywordOption():
                    parser.eat()
                    prog.flags_and_options.append(Option._parse(parser))

                case KeywordStruct():
                    parser.eat()
                    prog.user_types.append(StructDefinition._parse(parser))

                case KeywordEnum():
                    parser.eat()
                    prog.user_types.append(EnumDefinition._parse(parser))

                case KeywordUse():
                    parser.eat(2)

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing program body"
                    )

            if parser.peek(0) != LineEnd():
                raise BirdwaySyntaxError(
                    f"missing semicolon on line {parser.peek(0)._line}"
                )
            parser.eat()

        return prog
