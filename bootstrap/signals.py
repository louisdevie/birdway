class Signal(Exception):
    pass


class ErrorSignal(Signal):
    pass


class FailSignal(ErrorSignal):
    pass


class OSErrorSignal(ErrorSignal):
    pass


class NotFoundErrorSignal(OSErrorSignal):
    pass


global_error_message = None
