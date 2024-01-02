# The various other things that fit nowhere else

DEFAULT_EPS = 1e-6

def float_equal(a: float, b: float) -> bool:
    return True if (abs(a-b) < DEFAULT_EPS) else False


def load_source(filename:str) -> str:
    with open(filename, 'r') as fp:
        source = fp.read()
    return str(source)

