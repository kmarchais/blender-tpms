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


def honeycomb_gyroid(x: float, y: float, z: float) -> float:
    return sin(x) * cos(y) + sin(y) + cos(x)


def honeycomb_primitive(x: float, y: float, z: float) -> float:
    return cos(x) + cos(y)

def honeycomb_diamond(x, y, z):
    return cos(x) * cos(y) + sin(x) * sin(y) + sin(x) * cos(y) + cos(x) * sin(y)

def honeycomb_I(x, y, z):
    return cos(x) * cos(y) + cos(y) + cos(x)

def honeycomb_L(x, y, z):
    return (
        1.1 * (sin(2 * x) * cos(y) + sin(2 * y) * sin(x) + cos(x) * sin(y)) - 
        (cos(2 * x) * cos(2 * y) + cos(2 * y) + cos(2 * x))
    )

def SC(x, y, z):
    return (
        2 * (cos(x) + cos(y) + cos(z)) +
        cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x)
    )

def I(x, y, z):
    return cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x)

def P(x, y, z):
    return sin(x) + sin(y) + sin(z)


def P_W(x, y, z):
    return 4 * (cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x)) - 3 * cos(x) * cos(y) * cos(z)


def double_gyroid(x, y, z):
    return (
        2.75 * (sin(2 * x) * sin(z) * cos(y) +
                sin(2 * y) * sin(x) * cos(z) +
                sin(2 * z) * sin(y) * cos(x)) -
        (cos(2 * x) * cos(2 * y) +
         cos(2 * y) * cos(2 * z) +
         cos(2 * z) * cos(2 * x))
    )


def Gprime(x, y, z):
    return (
        5 * (sin(2 * x) * sin(z) * cos(y) +
             sin(2 * y) * sin(x) * cos(z) +
             sin(2 * z) * sin(y) * cos(x)) +
        cos(2 * x) * cos(2 * y) +
        cos(2 * y) * cos(2 * z) +
        cos(2 * z) * cos(2 * x)
    )


def double_diamond(x, y, z):
    return (
        sin(2 * x) * sin(2 * y) +
        sin(2 * y) * sin(2 * z) +
        sin(2 * x) * sin(2 * z) +
        cos(2 * x) * cos(2 * y) * cos(2 * z)
    )


def Dprime(x, y, z):
    return (
        sin(x) * sin(y) * sin(z) +
        cos(x) * cos(y) * cos(z) -
        (cos(2 * x) * cos(2 * y) +
            cos(2 * y) * cos(2 * z) +
            cos(2 * z) * cos(2 * x)) - 0.4
    )


def doubleP(x, y, z):
    return (
        0.5 * (cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x)) +
        0.2 * (cos(2 * x) + cos(2 * y) + cos(2 * z))
    )


def OCTO(x, y, z):
    return (
        4 * (cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x)) -
        2.8 * cos(x) * cos(y) * cos(z) +
        (cos(x) + cos(y) + cos(z)) + 1.5
    )


def PN(x, y, z):
    return (
        0.6*(cos(x)*cos(y)*cos(z)) +
        0.4*(cos(x) + cos(y) + cos(z)) +
        0.2*(cos(2*x)*cos(2*y)*cos(2*z)) +
        0.2*(cos(2*x) + cos(2*y) + cos(2*z)) +
        0.1*(cos(3*x) + cos(3*y) + cos(3*z)) +
        0.2*(cos(x)*cos(y) + cos(y)*cos(z) + cos(z)*cos(x))
    )


def KP(x, y, z):
    return (
        0.6*(cos(x) + cos(y) + cos(z)) +
        0.7*(cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x)) -
        0.9*(cos(2 * x) * cos(2 * y) * cos(2 * z)) + 0.4
    )


def FRD(x, y, z):
    return (
        8 * cos(x) * cos(y) * cos(z) +
        cos(2 * x) * cos(2 * y) * cos(2 * z) -
        cos(2 * x) * cos(2 * y) +
        cos(2 * y) * cos(2 * z) +
        cos(2 * z) * cos(2 * x)
    )


def splitP(x, y, z):
    return (
        1.1 * (sin(2 * x) * sin(z) * cos(y) +
               sin(2 * y) * sin(x) * cos(z) +
               sin(2 * z) * sin(y) * cos(x)) -
        0.2 * (cos(2 * x) * cos(2 * y) +
               cos(2 * y) * cos(2 * z) +
               cos(2 * z) * cos(2 * x)) -
        0.4 * (cos(x) + cos(y) + cos(z))
    )
