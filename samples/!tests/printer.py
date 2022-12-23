__all__ = ["Printer", "YELLOW", "GREEN", "RED", "LIGHTRED", "BOLD", "RESET"]


class Printer:
    def __init__(self, stream):
        self.__out = stream
        self.__indent = list()
        self.__newline = True

    def print(self, *objects, sep=" ", style=None):
        if self.__newline:
            self.__out.write("".join(self.__indent))
            self.__newline = False

        if style is not None:
            self.__out.write(style.escape)

        self.__out.write(sep.join(str(obj) for obj in objects))

        if style is not None:
            self.__out.write(RESET.escape)

    def println(self, *objects, sep=" ", style=None):
        self.print(*objects, sep=sep, style=style)
        self.newline()

    def newline(self):
        if not self.__newline:
            self.__out.write("\n")
            self.__newline = True

    def indent(self, indent="   "):
        self.__indent.append(indent)

    def unindent(self):
        return self.__indent.pop(-1)


class Style:
    def __init__(self, escape_code, category):
        self.__esc = escape_code
        self.__cat = category

    def __and__(lhs, rhs):
        if not isinstance(rhs, Style):
            return NotImplemented

        if (lhs.__cat & rhs.__cat) != 0:
            raise ValueError(f"cannot combine two styles of the same category")

        return Style(lhs.__esc + ";" + rhs.__esc, lhs.__cat + rhs.__cat)

    @property
    def escape(self):
        return "\x1b[" + self.__esc + "m"


YELLOW = Style("93", 1)
GREEN = Style("32", 1)
RED = Style("31", 1)
LIGHTRED = Style("91", 1)
BOLD = Style("1", 2)
RESET = Style("0", 3)
