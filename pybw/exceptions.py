class BirdwayCompilationError(Exception):
    pass


class BirdwaySyntaxError(BirdwayCompilationError):
    pass


class BirdwayNameError(BirdwayCompilationError):
    pass


class BirdwayTypeError(BirdwayCompilationError):
    pass
