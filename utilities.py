from itertools import chain

def flatten(xs):
    match xs:
        case [x]: return x
        case [*xs]: return list(chain(*[x if isinstance(x, list) else [x] for x in xs]))
        case something: return something 

def fixed_point(f, x):
    applied = f(x)
    if x == applied:
        return x
    return fixed_point(f, applied)

def pipe(x, *functions):
    result = x
    for f in functions:
        result = f(result)
        if isinstance(result, Exception):
            return result
    return result