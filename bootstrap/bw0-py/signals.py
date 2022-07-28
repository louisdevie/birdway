class Signal:
    def __init__(self, code):
        self.__c = code

    def __eq__(lhs, rhs):
        if isinstance(rhs, Signal):
            return lsh.__c == rhs.__c
        else:
            return False


class Return(Signal):
    def __init__(self, value):
        super().__init__(-1)
        self.value = value


SIG_RETURN = Signal(-1)
