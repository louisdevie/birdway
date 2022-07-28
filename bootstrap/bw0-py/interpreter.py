from error import BirdwayNameError, BirdwayTypeError
from signals import *
from parser import Node
import predef
from operators import Value
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

    def __pop_context(self):
        self.__ctx.pop(0)

    def __resolve(self, name):
        for ctx in self.__ctx:
            if name in ctx:
                return ctx[name]
        raise BirdwayNameError(f"use of undeclared name ‘{name}’")

    def __load_global_context(self):
        self.__push_context()

        for func in self.__ast["functions"]:
            self.__declare_func(func["name"], func)

    def __call(self, name, *args):
        func = self.__resolve(name)

        if not isinstance(func, list):
            raise BirdwayTypeError(f"{name} is not a function")

        return self.__run_dispatch(func[0]["result"])

    def __run_dispatch(self, obj):
        match obj["node"]:
            case Node.PRINT:
                return self.__run_print(obj)

            case Node.STRING:
                return self.__run_string(obj)

            case other:
                raise NotImplementedError(f"{other} not implemented")

    def __run_string(self, string):
        return Value(Str(), string["content"][0])

    def __run_print(self, prints):
        content = self.__run_dispatch(prints["content"])

        print(predef.to_string(content).internal_object)

        return Value(Void(), None)
