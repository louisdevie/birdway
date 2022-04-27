from autorepr import AutoRepr, PrettyAutoRepr
from tokens import *
from birdway import ArgumentModifier, Type
from exceptions import *
from enum import Enum, auto

from nodes import *


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

    def pop(self):
        return self.tokens.pop(0)

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

                case KeywordParam():
                    self.eat()
                    prog.arguments.append(self.parse_parameter())
                    if self.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(
                            f"missing semicolon on line {self.peek(0)._line} after parameter"
                        )
                    self.eat()

                case KeywordRun():
                    self.eat()
                    if self.peek(0) == BlockBegin():
                        self.eat()
                        prog.script = self.parse_block()
                    else:
                        prog.script = self.parse_expression()
                    if self.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(
                            f"missing semicolon on line {self.peek(0)._line}"
                        )
                    self.eat()

                case KeywordOption():
                    self.eat()
                    prog.arguments.append(self.parse_parameter())
                    if self.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(
                            f"missing semicolon on line {self.peek(0)._line} after parameter"
                        )
                    self.eat()

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing program body"
                    )

        return prog

    def parse_expression(self):
        match self.peek(0):
            case TableBegin():
                self.eat()
                lhs = self.parse_table()

            case StringDelimiter():
                self.eat()
                lhs = self.parse_string()

            case FormattedStringDelimiter():
                self.eat()
                lhs = self.parse_formatted_string()

            case KeywordIf():
                self.eat()
                lhs = self.parse_if()

            case KeywordPrintln():
                self.eat()
                lhs = self.parse_println()

            case Identifier(name=var):
                self.eat()
                lhs = ReadVariable()
                lhs.name = var

            case BlockBegin():
                self.eat()
                lhs = self.parse_block()

            case UnaryOperator(operator=op):
                self.eat()
                operation = UnaryOperation()
                operation.operator = op
                operation.operand = self.parse_expression()
                return operation

            case other:
                raise BirdwaySyntaxError(
                    f"unexpected {other} at line {other._line} while parsing expression"
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

            if self.peek(0) == Separator():
                self.eat()
                if self.peek(0) == TableEnd():
                    self.eat()
                    return table
            else:
                if self.peek(0) == TableEnd():
                    self.eat()
                    return table
                else:
                    raise BirdwaySyntaxError(f"expected colon between values of table (line {self.peek(0)._line})")


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
                    literal = StringLiteral()
                    literal.string = val
                    string.content.append(literal)

                case Variable(name=var):
                    self.eat()
                    formatting = ReadVariable()
                    formatting.name = var
                    string.content.append(formatting)

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing string"
                    )

        raise BirdwaySyntaxError("hit EOF while parsing string")

    def parse_string(self):
        string = StringLiteral()

        while self.remaining():
            match self.peek(0):
                case StringDelimiter():
                    self.eat()
                    return string

                case StringContent(value=val):
                    self.eat()
                    string.string += val

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing string"
                    )

        raise BirdwaySyntaxError("hit EOF while parsing string")

    def parse_parameter(self):
        parameter = Parameter()

        match self.peek(0):
            case TypeName(type=t):
                self.eat()
                parameter.type = t

            case other:
                raise BirdwaySyntaxError(
                    f"expected type, got {other} at line {other._line}"
                )

        if self.peek(0) == UnaryOperator(operator=Unary.ISDEF):
            self.eat()
            parameter.modifier = ArgumentModifier.OPTIONAL

        match self.peek(0):
            case Identifier(name=ident):
                self.eat()
                parameter.name = ident

            case other:
                raise BirdwaySyntaxError(
                    f"expected identifier or modifier, got {other} at line {other._line}"
                )

        if self.peek(0) == FormattedStringDelimiter():
            self.eat()
            parameter.description = self.parse_formatted_string()
        elif self.peek(0) == StringDelimiter():
            self.eat()
            parameter.description = self.parse_string()

        return parameter

    def parse_block(self):
        block = Block()

        while self.remaining():
            match self.peek(0):
                case BlockEnd():
                    self.eat()
                    return block

                case _:
                    block.statements.append(self.parse_expression())
                    if self.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(
                            f"missing semicolon on line {self.peek(0)._line}"
                        )
                    self.eat()

        raise BirdwaySyntaxError("hit EOF while parsing block")

    def parse_if(self):
        ifthenelse = IfThenElse()

        ifthenelse.condition = self.parse_expression()

        tok = self.pop()
        if tok != KeywordThen():
            raise BirdwaySyntaxError(
                f"expected keyword then, got {tok} on line {tok._line}"
            )

        ifthenelse.statements = self.parse_expression()

        if self.peek(0) == KeywordElse():
            self.eat()
            ifthenelse.alternative = self.parse_expression()

        return ifthenelse

    def parse_println(self):
        println = PrintLine()

        println.content = self.parse_expression()

        return println
