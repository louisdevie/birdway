def count(iterable, predicate):
    c = 0
    for item in iterable:
        if predicate(item):
            c += 1
    return c
