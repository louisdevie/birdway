class AutoRepr:
    def __repr__(self):
        return (
            type(self).__name__
            + "("
            + ", ".join(
                [
                    attr + "=" + repr(getattr(self, attr))
                    for attr in dir(self)
                    if not attr.startswith("_")
                ]
            )
            + ")"
        )
