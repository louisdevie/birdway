import enum

from error import BirdwaySyntaxError
from lexer import *
from birdway_types import *


class Node(enum.Enum):
    FUNCDEF = enum.auto()
    PRINT = enum.auto()
    STRING = enum.auto()


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

            if (invalid := self.pop()) != Symbol(";"):
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

        if (invalid := self.pop()) != Symbol(":"):
            raise BirdwaySyntaxError(f"expected colon, got {invalid}")

        option["type"] = self.__parse_type()

        if self.peek() == Operator("="):
            self.pop()
            option["default"] = self.__parse_expression()

        return option

    def __parse_param(self):
        param = {}

        match self.pop():
            case Identifier(name):
                param["name"] = name

            case other:
                raise BirdwaySyntaxError(f"expected parameter name, got {other}")

        if (invalid := self.pop()) != Symbol(":"):
            raise BirdwaySyntaxError(f"expected colon, got {invalid}")

        param["type"] = self.__parse_type()

        return param

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

            case StringDelitmiter():
                self.pop()
                lhs = self.__parse_string_literal()

            case other:
                raise BirdwaySyntaxError(f"unexpected {other} while parsing expression")

        return lhs

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
        prints = {"node": Node.PRINT, "line": ln}

        prints["content"] = self.__parse_expression()

        return prints

    def __parse_function(self):
        function = {"node": Node.FUNCDEF}

        match self.pop():
            case Identifier(name):
                function["name"] = name

            case other:
                raise BirdwaySyntaxError(f"expected parameter name, got {other}")

        if (invalid := self.pop()) != Symbol("("):
            raise BirdwaySyntaxError(f"expected ‘(’, got {invalid}")

        while self.peek() != Symbol(")"):
            ...

        self.pop()

        if (invalid := self.pop()) != Symbol("->"):
            raise BirdwaySyntaxError(f"expected ‘->’, got {invalid}")

        function["result"] = self.__parse_expression()

        return function
