def same(iterable):
    if len(iterable) != 0:
        ref = iterable[0]
        for val in iterable:
            if val != ref:
                return False
    return True
