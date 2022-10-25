import sys

from error import BirdwayNameError, BirdwayTypeError
from signals import *
from parser import Node
import predef
from operators import Value, OP_BIN
from birdway_types import *


class Interpreter:
    def __init__(self, ast):
        self.__ast = ast
        self.__stack = list()
        self.__ctx = list()

    def run(self):
        self.__load_global_context()
        self.__call("main")

    def __push_context(self):
        self.__ctx.insert(0, dict())

    def __declare(self, name, obj):
        self.__ctx[0][name] = obj

    def __declare_func(self, name, obj):
        if name in self.__ctx[0]:
            self.__ctx[0][name].append(obj)
        else:
            self.__ctx[0][name] = [obj]

    def __declare_var(self, name, type, value, mut):
        if name in self.__ctx[0]:
            raise BirdwayNameError(f"{name} already exists")
        else:
            self.__ctx[0][name] = Storage(type, value, mut, name)

    def __pop_context(self):
        self.__ctx.pop(0)

    def resolve(self, name):
        for ctx in self.__ctx:
            if name in ctx:
                return ctx[name]
        if name in predef.NAMES:
            return predef.NAMES[name]
        raise BirdwayNameError(f"use of undeclared ‘{name}’")

    def __load_global_context(self):
        self.__push_context()

        for func in self.__ast["functions"]:
            self.__declare_func(func["name"], func)

        for i, param in enumerate(self.__ast["parameters"]):
            self.__declare_var(param["name"], Str(), sys.argv[i + 2], False)

    def __call(self, name, *args):
        func = self.resolve(name)

        if isinstance(func, list):
            return self.run_dispatch(func[0]["result"])

        elif callable(func):
            return func(*args)

        else:
            raise BirdwayTypeError(f"{name} is not a function")

    def __read(self, name):
        return self.resolve(name).get()

    def run_dispatch(self, obj):
        match obj["node"]:
            case Node.PRINT:
                return self.__run_print(obj)

            case Node.STRING:
                return self.__run_string(obj)

            case Node.BLOCK:
                return self.__run_block(obj)

            case Node.BINOP:
                return self.__run_binop(obj)

            case Node.FUNCCALL:
                return self.__run_fcall(obj)

            case Node.NAME:
                return self.__run_name(obj)

            case Node.LETVAR:
                return self.__run_var(obj)

            case Node.TRY:
                return self.__run_try(obj)

            case Node.READ:
                return self.__run_read(obj)

            case Node.THROW:
                return self.__run_throw(obj)

            case other:
                raise NotImplementedError(f"{other} not implemented")

    def __run_string(self, string):
        return Value(Str(), string["content"][0])

    def __run_print(self, prints):
        content = self.run_dispatch(prints["content"])
        dest = self.run_dispatch(prints["destination"])

        dest.internal_object.write(
            predef.to_string(content).internal_object + ("\n" if prints["line"] else "")
        )

        return Value(Void(), None)

    def __run_block(self, block):
        self.__push_context()

        for line in block["lines"]:
            self.run_dispatch(line)

        self.__pop_context()

        return Value(Void(), None)

    def __run_binop(self, op):
        return OP_BIN[op["op"]](op["lhs"], op["rhs"], self)

    def __run_fcall(self, fcall):
        args = (self.run_dispatch(a) for a in fcall["args"])
        return self.__call(fcall["func"]["name"], *args)

    def __run_name(self, name):
        return self.__read(name["name"])

    def __run_var(self, var):
        init_value = self.run_dispatch(var["value"])

        self.__declare_var(
            var["name"], init_value.type, init_value.internal_object, var["mutable"]
        )

    def __run_try(self, trys):
        try:
            self.run_dispatch(trys["try"])
        except ErrorSignal as err:
            for h, r in trys["handlers"]:
                handler = self.run_dispatch(h)
                if isinstance(err, handler.internal_object):
                    self.run_dispatch(r)
                    break

    def __run_throw(self, throw):
        raise self.run_dispatch(throw["signal"]).internal_object

    def __run_read(self, read):
        if read["line"]:
            raise NotImplementedError("readln isn't implemented")

        else:
            source = self.run_dispatch(read["source"])

            return Value(Str(), source.internal_object.read())


class Storage:
    def __init__(self, type, value, is_mut, name):
        self.__type = type
        self.__mut = is_mut
        self.__val = value
        self.__name = name

    def get(self):
        return Value(self.__type, self.__val)

    def set(self, type, new_val):
        if self.__mut:
            if type == self.__type:
                self.__val = new_val
            else:
                raise BirdwayTypeError(
                    f"cannot assign {type} value to {self.__type} variable"
                )
        else:
            raise BirdwayTypeError(
                f"can't set constant or immutable variable {self.name}"
            )
