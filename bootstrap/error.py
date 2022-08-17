class BirdwayError(Exception):
    pass


class BirdwayLexicalError(BirdwayError):
    pass


class BirdwaySyntaxError(BirdwayError):
    pass


class BirdwayNameError(BirdwayError):
    pass


class BirdwayTypeError(BirdwayError):
    pass
