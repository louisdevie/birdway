from enum import Enum


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
