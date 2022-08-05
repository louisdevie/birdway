import enum

from error import BirdwaySyntaxError
from lexer import *
from birdway_types import *


class Node(enum.Enum):
    FUNCDEF = enum.auto()
    FUNCCALL = enum.auto()
    BLOCK = enum.auto()
    BINOP = enum.auto()
    PRINT = enum.auto()
    STRING = enum.auto()
    NAME = enum.auto()
    LETVAR = enum.auto()


class Parser:
    def __init__(self, tokens):
        self.__tokens = tokens
        self.__buffer = None

    def pop(self):
        if self.__buffer is None:
            return next(self.__tokens)
        else:
            b = self.__buffer
            self.__buffer = None
            return b

    def peek(self):
        if self.__buffer is None:
            self.__buffer = next(self.__tokens)

        return self.__buffer

    def parse(self):
        return self.__parse_body()

    def __parse_body(self):
        prog = {
            "metadata": [],
            "uses": [],
            "functions": [],
            "types": [],
            "parameters": [],
            "flags_options": [],
        }

        while True:
            match self.peek():
                case Keyword(keyword="meta"):
                    self.pop()
                    prog["metadata"].append(self.__parse_meta())

                case Keyword(keyword="use"):
                    self.pop()
                    match self.pop():
                        case Identifier(name):
                            prog["uses"].append(name)

                        case other:
                            raise BirdwaySyntaxError(
                                f"expected extension name, got {other}"
                            )

                case Keyword(keyword="option"):
                    self.pop()
                    prog["metadata"].append(self.__parse_option())

                case Keyword(keyword="param"):
                    self.pop()
                    prog["parameters"].append(self.__parse_param())

                case Keyword(keyword="func"):
                    self.pop()
                    prog["functions"].append(self.__parse_function())

                case EndOfFile():
                    self.pop()
                    break

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} while parsing program body"
                    )

            if (invalid := self.pop()) != Punctuation(";"):
                raise BirdwaySyntaxError(f"missing semicolon before {invalid}")

        return prog

    def __parse_meta(self):
        meta = {}

        match self.pop():
            case Identifier(name):
                meta["key"] = name

            case other:
                raise BirdwaySyntaxError(f"expected metadata key, got {other}")

        if (invalid := self.pop()) != Operator("="):
            raise BirdwaySyntaxError(f"expected equal sign, got {invalid}")

        meta["value"] = self.__parse_expression()

        return meta

    def __parse_option(self):
        option = {"isflag": False}

        match self.pop():
            case Identifier(name):
                option["name"] = name

            case other:
                raise BirdwaySyntaxError(f"expected option name, got {other}")

        if (invalid := self.pop()) != Punctuation(":"):
            raise BirdwaySyntaxError(f"expected colon, got {invalid}")

        option["type"] = self.__parse_type()

        if self.peek() == Operator("="):
            self.pop()
            option["default"] = self.__parse_expression()

        return option

    def __parse_param(self):
        param = {"modifier": "none"}

        if self.peek() == Operator("?"):
            self.pop()
            param["modifier"] = "optional"

        match self.pop():
            case Identifier(name):
                param["name"] = name

            case other:
                raise BirdwaySyntaxError(f"expected parameter name, got {other}")

        if (invalid := self.pop()) != Punctuation(":"):
            raise BirdwaySyntaxError(f"expected colon, got {invalid}")

        param["type"] = self.__parse_type()

        if self.peek() == Punctuation("("):
            self.pop()
            param["description"] = self.__parse_expression()

            if (invalid := self.pop()) != Punctuation(")"):
                raise BirdwaySyntaxError(
                    f"missing closing parenthesis before {invalid}"
                )

        return param

    def __parse_comma_separated_values(self, context, end, value):
        values = []

        while True:
            if self.peek() == end:
                self.pop()
                return values

            values.append(value())

            if (invalid := self.pop()) != Punctuation(","):
                if invalid == end:
                    return values
                raise BirdwaySyntaxError(f"missing comma before {invalid}")

    def __parse_type(self):
        match self.pop():
            case Primitive(name):
                match name:
                    case "Str":
                        t = Str()
                    case other:
                        raise NotImplementedError(f"unhandled primitive type {other}")

            case other:
                raise BirdwaySyntaxError(f"unexpected {other} while parsing type")

        return t

    def __parse_expression(self):
        match self.peek():
            case Keyword(keyword="println"):
                self.pop()
                lhs = self.__parse_print(ln=True)

            case Keyword(keyword="try"):
                self.pop()
                lhs = self.__parse_try()

            case StringDelitmiter():
                self.pop()
                lhs = self.__parse_string_literal()

            case Punctuation("{"):
                self.pop()
                lhs = self.__parse_block()

            case Identifier(name=name):
                self.pop()
                lhs = {"node": Node.NAME, "name": name}

            case other:
                raise BirdwaySyntaxError(f"unexpected {other} while parsing expression")

        match self.peek():
            case Operator(operator="&&"):
                op = self.pop().operator
                return {
                    "node": Node.BINOP,
                    "op": op,
                    "lhs": lhs,
                    "rhs": self.__parse_expression(),
                }

            case Punctuation("("):
                self.pop()
                return {
                    "node": Node.FUNCCALL,
                    "func": lhs,
                    "args": self.__parse_comma_separated_values(
                        end=Punctuation(")"),
                        context="function arguments",
                        value=self.__parse_expression,
                    ),
                }

        return lhs

    def __parse_block(self):
        block = {"node": Node.BLOCK, "lines": []}

        while True:
            match self.peek():
                case Keyword(keyword="func"):
                    self.pop()
                    block["lines"].append(self.__parse_function())

                case Keyword(keyword="let"):
                    self.pop()
                    block["lines"].append(self.__parse_variable())

                case EndOfFile():
                    raise BirdwaySyntaxError(f"hit EOF while parsing block")

                case other:
                    block["lines"].append(self.__parse_expression())

            if (invalid := self.pop()) != Punctuation(";"):
                raise BirdwaySyntaxError(f"missing semicolon before {invalid}")

        return prog

    def __parse_string_literal(self):
        string = {
            "node": Node.STRING,
            "content": [],
        }

        while True:
            match self.peek():
                case Text(text):
                    self.pop()
                    string["content"].append(text)

                case StringDelitmiter():
                    self.pop()
                    break

                case EndOfFile():
                    raise BirdwaySyntaxError(f"hit EOF while parsing string literal")

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} while parsing string literal"
                    )

        return string

    def __parse_print(self, ln=False):
        print_ = {"node": Node.PRINT, "line": ln}

        print_["content"] = self.__parse_expression()

        return print_

    def __parse_try(self):
        try_ = {"node": Node.TRY}

        print_["try"] = self.__parse_expression()

    def __parse_function(self):
        function = {"node": Node.FUNCDEF}

        match self.pop():
            case Identifier(name):
                function["name"] = name

            case other:
                raise BirdwaySyntaxError(f"expected function name, got {other}")

        if (invalid := self.pop()) != Punctuation("("):
            raise BirdwaySyntaxError(f"expected ‘(’, got {invalid}")

        while self.peek() != Punctuation(")"):
            ...

        self.pop()

        if (invalid := self.pop()) != Punctuation("->"):
            raise BirdwaySyntaxError(f"expected ‘->’, got {invalid}")

        function["result"] = self.__parse_expression()

        return function

    def __parse_variable(self):
        variable = {"node": Node.LETVAR, "mutable": False}

        if self.peek() == Punctuation("$"):
            self.pop()
            variable["mutable"] = True

        match self.pop():
            case Identifier(name):
                variable["name"] = name

            case other:
                raise BirdwaySyntaxError(f"expected variable name, got {other}")

        if (invalid := self.pop()) != Operator("="):
            raise BirdwaySyntaxError(f"expected ‘=’, got {invalid}")

        variable["value"] = self.__parse_expression()

        return variable
