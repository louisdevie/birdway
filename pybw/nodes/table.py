from .base import *


from .string_literal import StringLiteral
from .range import Range
from birdway import FEATURE_TABLE


class Table(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.key_type = None
        self.value_type = Type.UNKNOWN
        self.values = dict()

    @classmethod
    def _parse(cls, parser):
        table = cls()

        while parser.remaining():
            val_or_key = parser.parse_expression()

            if parser.peek(0) == Association():
                parser.eat()
                val = parser.parse_expression()

                if table.key_type == None:
                    table.key_type = val_or_key.type
                else:
                    if val_or_key.type != table.key_type:
                        raise BirdwayTypeError(
                            f"inconsistent table keys types (expected {table.key_type}, found {val_or_key.type}) around {parser.peek(0)._line}"
                        )

                if table.value_type == Type.UNKNOWN:
                    table.value_type = val.type
                else:
                    if val.type != table.value_type:
                        raise BirdwayTypeError(
                            f"inconsistent table values types (expected {table.value_type}, found {val.type}) around {parser.peek(0)._line}"
                        )

                table.values[val_or_key] = val

            elif parser.peek(0) == RangeSymbol():
                parser.eat()

                r = Range()
                r.start = val_or_key

                r.end = parser.parse_expression()

                if table.value_type == Type.UNKNOWN:
                    table.value_type = val_or_key.type
                else:
                    if val_or_key.type != table.value_type:
                        raise BirdwayTypeError(
                            f"inconsistent table values types (expected {table.value_type}, found {val.type})"
                        )

                table.values[r] = None

            else:
                if table.value_type == Type.UNKNOWN:
                    table.value_type = val_or_key.type
                else:
                    if val_or_key.type != table.value_type:
                        raise BirdwayTypeError(
                            f"inconsistent table values types (expected {table.value_type}, found {val.type})"
                        )

                table.values[val_or_key] = None

            if parser.peek(0) == Separator():
                parser.eat()
                if parser.peek(0) == TableEnd():
                    parser.eat()
                    return table
            else:
                if parser.peek(0) == TableEnd():
                    parser.eat()
                    return table
                else:
                    raise BirdwaySyntaxError(
                        f"expected colon between values of table (line {parser.peek(0)._line})"
                    )

        raise BirdwaySyntaxError("hit EOF while parsing table")

    def _type(self):
        return Composite.Table(self.value_type, self.key_type)

    def _propagate(self, ast, vc, lc, bc):
        ast.standard_features |= FEATURE_TABLE
        for val in self.values:
            val.context = self.context.copy()
            self.using |= val._propagate(ast, vc, lc, bc)
        return self.using

    def _check(self):
        pass
