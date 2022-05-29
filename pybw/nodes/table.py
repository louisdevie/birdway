from .base import *


from .string_literal import StringLiteral
from .range import Range


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
                table.values[val_or_key] = val
                table.key_type = Type.UNKNOWN

            elif table.key_type == Type.UNKNOWN:
                raise BirdwaySyntaxError(
                    f"missing colon in dictionary table (line {parser.peek(0)._line})"
                )

            elif parser.peek(0) == RangeSymbol():
                parser.eat()

                r = Range()
                r.start = val_or_key

                r.end = parser.parse_expression()

                table.values[r] = None

            else:
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
        if self.key_type is None:
            for val in self.values:
                if self.value_type == Type.UNKNOWN:
                    self.value_type = val.type
                else:
                    if val.type != self.value_type:
                        raise BirdwayTypeError(
                            f"inconsistent table value types (expected {self.value_type}, found {val.type})"
                        )
        else:
            for key, val in self.values.items():
                if self.key_type == Type.UNKNOWN:
                    self.key_type = key.type
                else:
                    if key.type != self.key_type:
                        raise BirdwayTypeError(
                            f"inconsistent table key types (expected {self.key_type}, found {key.type})"
                        )
                if self.value_type == Type.UNKNOWN:
                    self.value_type = val.type
                else:
                    if val.type != self.value_type:
                        raise BirdwayTypeError(
                            f"inconsistent table value types (expected {self.value_type}, found {val.type})"
                        )

        if self.key_type is None:
            ast.table_list_types.append(self.value_type)
        for val in self.values:
            val.context = self.context.copy()
            self.using |= val._propagate(ast, vc, lc, bc)
        return self.using

    def _check(self):
        if self.key_type is None:
            for val in self.values:
                val._check()
        else:
            for key, val in self.values.items():
                key._check()
                val._check()

    def _initialise(self):
        return "".join([k._initialise() for k in self.values.keys()])

    def _transpile(self, tui):
        return f"""
            {ctype(self.type)}{tui} = {{NULL, NULL, 0, -1}};
            {"".join([
                (
                    val._transpile(tui + str(i))
                    + f"for (int val=({val.start._reference(tui + str(i) + '1')});"
                    + f"val<=({val.end._reference(tui + str(i) + '2')});val++)"
                    + "{birdwayListTableAppend" + nameof(self.value_type)
                    + "(&" + tui + ", val);}"
                ) if isinstance(val, Range) else (
                    val._transpile(tui + str(i))
                    + "birdwayListTableAppend" + nameof(self.value_type)
                    + "(&" + tui + "," + val._reference(tui + str(i)) + ");"
                ) 
                for i, val in enumerate(self.values)
            ])}"""
