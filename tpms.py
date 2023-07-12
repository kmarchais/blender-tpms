from numpy import pi, sin, cos

def gyroid(x, y, z):
    return (
        sin(x) * cos(y)
        + sin(y) * cos(z)
        + sin(z) * cos(x)
    )
    
def schwarzP(x: float, y: float, z: float) -> float:
    return cos(x) + cos(y) + cos(z)


def schwarzD(x: float, y: float, z: float) -> float:
    a = sin(x) * sin(y) * sin(z)
    b = sin(x) * cos(y) * cos(z)
    c = cos(x) * sin(y) * cos(z)
    d = cos(x) * cos(y) * sin(z)
    return a + b + c + d


def neovius(x: float, y: float, z: float) -> float:
    a = 3 * cos(x) + cos(y) + cos(z)
    b = 4 * cos(x) * cos(y) * cos(z)

    return a + b


def schoenIWP(x: float, y: float, z: float) -> float:
    a = 2 * (
        cos(x) * cos(y)
        + cos(y) * cos(z)
        + cos(z) * cos(x)
    )
    b = cos(2 * x) + cos(2 * y) + cos(2 * z)

    return a - b


def schoenFRD(x: float, y: float, z: float) -> float:
    a = 4 * cos(x) * cos(y) * cos(z)
    b = (
        cos(2 * x) * cos(2 * y)
        + cos(2 * y) * cos(2 * z)
        + cos(2 * z) * cos(2 * x)
    )
    return a - b


def fischerKochS(x: float, y: float, z: float) -> float:
    a = cos(2 * x) * sin(y) * cos(z)
    b = cos(x) * cos(2 * y) * sin(z)
    c = sin(x) * cos(y) * cos(2 * z)

    return a + b + c


def pmy(x: float, y: float, z: float) -> float:
    a = 2 * cos(x) * cos(y) * cos(z)
    b = sin(2 * x) * sin(y)
    c = sin(x) * sin(2 * z)
    d = sin(2 * y) * sin(z)

    return a + b + c + d


def honeycomb(x: float, y: float, z: float) -> float:
    return sin(x) * cos(y + pi / 2.0) + sin(y + pi / 2.0) + cos(z)


def lidinoid(x: float, y: float, z: float) -> float:
    return 0.5 * (sin(2 * x) * cos(y) * sin(z) +
                  sin(2 * y) * cos(z) * sin(x) +
                  sin(2 * z) * cos(x) * sin(y)) - \
           0.5 * (cos(2 * x) * cos(2 * y) +
                  cos(2 * y) * cos(2 * z) +
                  cos(2 * z) * cos(2 * x)) + 0.3


def split_p(x: float, y: float, z: float) -> float:
    return 1.1 * (sin(2 * x) * cos(y) * sin(z) +
                  sin(2 * y) * cos(z) * sin(x) +
                  sin(2 * z) * cos(x) * sin(y)) - \
           0.2 * (cos(2 * x) * cos(2 * y) +
                  cos(2 * y) * cos(2 * z) +
                  cos(2 * z) * cos(2 * x)) - \
           0.4 * (cos(2 * x) + cos(2 * y) + cos(2 * z))

def gyroid_honeycomb(x: float, y: float, z: float) -> float:
    return gyroid(x, y, 0)

def primitive_honeycomb(x: float, y: float, z: float) -> float:
    return schwarzP(x, y, 0)
