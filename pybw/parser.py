from autorepr import AutoRepr, PrettyAutoRepr
from tokens import *
from exceptions import *
from nodes import *
from birdway import EnumPromise


def parse(tokens):
    parser = Parser(tokens)
    return Program._parse(parser)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def peek(self, pos=0):
        return self.tokens[pos]

    def eat(self, howmany=1):
        for _ in range(howmany):
            self.tokens.pop(0)

    def pop(self):
        return self.tokens.pop(0)

    def remaining(self):
        return len(self.tokens) > 0

    def parse_type(self):
        match self.peek(0):
            case TypeName(type=t):
                self.eat()
                return t

            case KeywordEnum():
                match self.peek(1):
                    case Identifier(name=ident):
                        self.eat(2)
                        return EnumPromise(ident)

                    case other:
                        raise BirdwaySyntaxError(
                            f"expected identifier after ‘enum’, got {other} at line {other._line}"
                        )

            case other:
                raise BirdwaySyntaxError(
                    f"expected type, got {other} at line {other._line}"
                )

    def parse_expression(self):
        match self.peek(0):
            case TableBegin():
                self.eat()
                lhs = Table._parse(self)

            case StringDelimiter():
                self.eat()
                lhs = StringLiteral._parse(self)

            case FormattedStringDelimiter():
                self.eat()
                lhs = self.parse_formatted_string()

            case KeywordIf():
                self.eat()
                lhs = self.parse_if()

            case KeywordFor():
                self.eat()
                lhs = ForLoop._parse(self)

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

            case KeywordFunc():
                self.eat()
                lhs = FunctionDefinition._parse(self)

            case Integer(value=val):
                self.eat()
                lhs = IntegerLiteral()
                lhs.value = val

            case other:
                raise BirdwaySyntaxError(
                    f"unexpected {other} at line {other._line} while parsing expression"
                )

        return lhs
