from enum import Enum
from birdway import Typed, Composite


class AutoRepr:
    def __repr__(self):
        return (
            type(self).__name__
            + "("
            + ", ".join(
                [
                    attr + "=" + self._smart_repr(getattr(self, attr))
                    for attr in dir(self)
                    if not attr.startswith("_")
                ]
            )
            + ")"
        )

    @staticmethod
    def _smart_repr(obj):
        if isinstance(obj, Enum):
            return str(obj)
        else:
            return repr(obj)


def indent(text):
    lines = text.split("\n")
    for i, old in enumerate(lines):
        lines[i] = "  " + old
    return "\n".join(lines)


class PrettyAutoRepr(AutoRepr):
    def __repr__(self):
        return (
            type(self).__name__
            + "(\n"
            + indent(
                ",\n".join(
                    [
                        attr + "=" + self._smart_repr(getattr(self, attr))
                        for attr in dir(self)
                        if not attr.startswith("_")
                    ]
                    + (
                        ["<" + self._smart_repr(getattr(self, "type")) + ">"]
                        if isinstance(self, Typed)
                        else []
                    )
                )
            )
            + "\n)"
        )

    @staticmethod
    def _smart_repr(obj):
        if (
            isinstance(obj, Enum)
            or isinstance(obj, Composite.Nullable)
            or isinstance(obj, Composite.Table)
        ):
            return str(obj)
        elif isinstance(obj, list):
            return (
                "[\n"
                + indent(",\n".join([PrettyAutoRepr._smart_repr(elem) for elem in obj]))
                + "\n]"
            )
        else:
            return repr(obj)
