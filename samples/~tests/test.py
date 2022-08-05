import yaml
import os, shutil
from pathlib import Path as P
from abc import ABC, abstractmethod
from printer import *

ENV = P(__file__).parent / "_testenv"


class TestABC(ABC):
    def __init__(self, ident):
        self.__id = ident

    @property
    def ident(self):
        return self.__id

    @abstractmethod
    def count_tests(self):
        ...

    @abstractmethod
    def run(self, p, r):
        ...


class SingleTest(TestABC):
    def __init__(self, ident, steps):
        super().__init__(ident)
        self.__steps = steps

    def count_tests(self):
        return 1

    @staticmethod
    def __err(msg, p):
        p.println(" FAIL", style=RED & BOLD)
        i = p.unindent()
        if i == "├─ ":
            p.indent("│     ")
        else:
            p.indent("      ")
        p.println(msg, style=LIGHTRED)
        p.unindent()
        p.indent(i)

    def run(self, p, r):
        p.print(self.ident, style=BOLD)

        used = list()

        if ENV.is_dir():
            shutil.rmtree(ENV)
        os.mkdir(ENV)

        try:
            for step, data in self.__steps:
                match step:
                    case "get":
                        file = data["get"]
                        fullpath = r / P(file)
                        if not fullpath.is_file():
                            self.__err(f"No such file : {file}", p)
                            return 0, used
                        shutil.copy(fullpath, ENV)
                        used.append(file)

        except Exception as err:
            self.__err(f"Unhandled exception : {err}", p)
            return 0, used

        p.println(" OK", style=GREEN & BOLD)
        return 1, used


class TestGroup(TestABC):
    def __init__(self, ident):
        super().__init__(ident)
        self.__tests = list()

    def count_tests(self):
        return sum(t.count_tests() for t in self.__tests)

    def run(self, p, r, asroot=False):
        if asroot:
            p.println("Tests")
        else:
            p.println("Group :", self.ident)

        modified_indent = None
        try:
            modified_indent = p.unindent()
            if modified_indent == "├─ ":
                p.indent("│  ")
            else:
                p.indent("   ")
        except IndexError:
            pass

        successful = 0
        files_used = []
        last = len(self.__tests) - 1
        p.indent("├─ ")
        for i, t in enumerate(sorted(self.__tests, key=lambda t: t.ident)):
            if i == last:
                p.unindent()
                p.indent("└─ ")
            s, f = t.run(p, r)
            successful += s
            files_used += f
        p.unindent()

        if modified_indent:
            p.unindent()
            p.indent(modified_indent)

        return successful, files_used

    def add(self, test):
        self.__tests.append(test)

    def subgroup(self, name):
        for t in self.__tests:
            if t.ident == name:
                if isinstance(t, TestGroup):
                    return t
                else:
                    raise NameError(f"{name} already exists and is a single test")

        new = TestGroup(name)
        self.add(new)
        return new


class Tests:
    def __init__(self):
        self.__tests = TestGroup("")

    def load(self, raw_yaml, src_path):
        data = yaml.safe_load(raw_yaml)
        for test in data:
            self.__insert_test(data[test], test, src_path.parts)

    def run(self, p, r):
        return self.__tests.run(p, r, True)

    def __insert_test(self, steps, name, groups_path):
        group = self.__tests
        for subgroup in groups_path:
            group = group.subgroup(subgroup)

        group.add(SingleTest(name, [self.__parse_step(s) for s in steps]))

    def __parse_step(self, data):
        for type_key in ["get", "compile", "run"]:
            if type_key in data:
                return (type_key, data)

    @property
    def count_total(self):
        return self.__tests.count_tests()


"""
┌ ─ ┬ ┐
│ │ │ │
├ ─ ┼ ┤
└ ─ ┴ ┘ 

Niv 1
├─ Niv 2
│  ├─ Niv 3
│  └─ Niv 3
└─ Niv 2
"""
