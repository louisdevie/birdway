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
                lhs = FormattedString._parse(self)

            case KeywordIf():
                self.eat()
                lhs = self.parse_if()

            case KeywordFor():
                self.eat()
                lhs = ForLoop._parse(self)

            case KeywordPrintln():
                self.eat()
                lhs = PrintLine._parse(self)

            case Identifier(name=var):
                self.eat()
                lhs = ReadVariable()
                lhs.name = var

            case BlockBegin():
                self.eat()
                lhs = Block._parse(self)

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

        match self.peek(0):
            case TableBegin():
                self.eat()
                ta = TableAccess()
                ta.table = lhs
                ta.index = self.parse_expression()
                if (invalid := self.pop()) != TableEnd():
                    raise BirdwaySyntaxError(
                            f"expected closing bracket, got {invalid} at line {invalid._line}"
                        )
                lhs = ta

            case OpeningParens():
                if not isinstance(lhs, ReadVariable):
                    raise BirdwaySyntaxError(f"unexpected parenthesis around line {self.peek(0)._line}")
                self.eat()
                fc = FunctionCall()
                fc.name = lhs.name

                while self.remaining():
                    fc.arguments.append(self.parse_expression())

                    if self.peek(0) == Separator():
                        self.eat()
                        if self.peek(0) == ClosingParens():
                            self.eat()
                            lhs = fc
                            break
                    else:
                        if self.peek(0) == ClosingParens():
                            self.eat()
                            lhs = fc
                            break
                        else:
                            raise BirdwaySyntaxError(
                                f"expected colon between function arguments (line {self.peek(0)._line})"
                            )
                else:
                    raise BirdwaySyntaxError("hit EOF while parsing function call")

        match self.peek(0):
            case BinaryOperator(operator = op):
                self.eat()
                expr = BinaryOperation()
                expr.operator = op
                expr.loperand = lhs
                expr.roperand = self.parse_expression()
                return expr

            case _:
                return lhs
