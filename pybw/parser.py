from autorepr import AutoRepr
from tokens import *
from birdway import Type
from exceptions import *
from enum import Enum, auto

class ArgumentModifier(Enum):
    NONE = auto()
    UNIQUE = auto()
    OPTIONAL = auto()
    VARIADIC = auto()

class Program(AutoRepr):
     def __init__(self):
        self.metadata = None
        self.arguments = None
        self.script = None

class Typed:
    def __getattr__(self, attr):
        if attr == 'type':
            return self._type()
        else:
            return super().__getattr__(attr)

    def _type(self):
        raise NotImplementedError()


class Table(AutoRepr, Typed):
    def __init__(self):
        self.key_type = Type.UNKNOWN
        self.value_type = Type.UNKNOWN
        self.values = dict()


class FormattedString(AutoRepr, Typed):
    def __init__(self):
        self.content = list()

    def _type(self):
        return Type.STRING


class Block(AutoRepr, Typed):
    def __init__(self):
        self.statements = list()

class Parameter(AutoRepr, Typed):
    def __init__(self):
        self.type = Type.UNKNOWN
        self.modifier = ArgumentModifier.NONE
        self.name = str()
        self.description = str()


def parse(tokens):
    parser = Parser(tokens)
    return parser.parse_program()


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def peek(self, pos):
        return self.tokens[0]

    def eat(self, howmany=1):
        for _ in range(howmany):
            self.tokens.pop(0)

    def remaining(self):
        return len(self.tokens) > 0

    def parse_program(self):
        prog = Program()

        while self.remaining():
            match self.peek(0):
                case KeywordMeta():
                    self.eat()
                    prog.metadata = self.parse_expression()
                    if self.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(
                            f"missing semicolon on line {self.peek(0)._line}"
                        )
                    self.eat()

                case KeywordArgs():
                    self.eat()
                    if self.peek(0) != BlockBegin():
                        raise BirdwaySyntaxError(
                            f"expected block on line {self.peek(0)._line}"
                        )
                    self.eat()
                    prog.arguments = self.parse_arguments_block()
                    if self.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(
                            f"missing semicolon on line {self.peek(0)._line}"
                        )
                    self.eat()

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing program body"
                    )

        return prog

    def parse_expression(self):
        if self.peek(0) == TableBegin():
            self.eat()
            lhs = self.parse_table()

        elif self.peek(0) == FormattedStringDelimiter():
            self.eat()
            lhs = self.parse_formatted_string()

        else:
            raise BirdwaySyntaxError(
                f"unexpected {self.peek(0)} at line {self.peek(0)._line} while parsing expression"
            )

        return lhs

    def parse_table(self):
        table = Table()

        while self.remaining():
            val_or_key = self.parse_expression()

            if self.peek(0) == Association():
                self.eat()
                val = self.parse_expression()

                if table.key_type == Type.UNKNOWN:
                    table.key_type = val_or_key.type
                else:
                    if val_or_key.type != table.key_type:
                        raise BirdwayTypeError(
                            f"inconsistent table keys types (expected {table.key_type}, found {val_or_key.type}) around {self.peek(0)._line}"
                        )

                if table.value_type == Type.UNKNOWN:
                    table.value_type = val.type
                else:
                    if val.type != table.value_type:
                        raise BirdwayTypeError(
                            f"inconsistent table values types (expected {table.value_type}, found {val.type}) around {self.peek(0)._line}"
                        )

                table.values[val_or_key] = val

            else:
                if table.key_type == Type.UNKNOWN:
                    table.key_type = val_or_key.type
                else:
                    if val_or_key.type != table.key_type:
                        raise BirdwayTypeError(
                            f"missing table keys around {self.peek(0)._line}"
                        )

                if table.value_type == Type.UNKNOWN:
                    table.value_type = val.type
                else:
                    if val.type != table.value_type:
                        raise BirdwayTypeError(
                            f"inconsistent table values types (expected {table.value_type}, found {val.type})"
                        )

                table.values[val_or_key] = val

            if self.peek(0) == TableEnd():
                self.eat()
                return table

        raise BirdwaySyntaxError("hit EOF while parsing table")

    def parse_formatted_string(self):
        string = FormattedString()

        while self.remaining():
            match self.peek(0):
                case FormattedStringDelimiter():
                    self.eat()
                    return string

                case StringContent(value=val):
                    self.eat()
                    string.content.append(val)

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing string"
                    )

        raise BirdwaySyntaxError("hit EOF while parsing string")

    def parse_arguments_block(self):
        block = Block()

        while self.remaining():
            match self.peek(0):
                case KeywordParam():
                    self.eat()
                    block.statements.append(self.parse_parameter())

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing arguments block"
                    )

        raise BirdwaySyntaxError("hit EOF while parsing arguments block")

    def parse_parameter(self):
        parameter = Parameter()

        match self.peek(0):
            case TypeName(type=t):
                self.eat()
                parameter.type = t

            case other:
                raise BirdwaySyntaxError(f"expected type, got {other} at line {other._line}") 

        if self.peek(0) == UnaryOperator(operator=Unary.ISDEF):
            self.eat()
            parameter.modifier = ArgumentModifier.OPTIONAL

        match self.peek(0):
            case Identifier(name=ident):
                self.eat()
                parameter.name = ident

            case other:
                raise BirdwaySyntaxError(f"expected identifier, got {other} at line {other._line}")

        if self.peek(0) == FormattedStringDelimiter():
            self.eat()
            parameter.description = self.parse_formatted_string()