"""Definition of the different TPMS surfaces."""

import numpy as np
from numpy import cos, pi, sin


def gyroid(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Gyroid surface."""
    return sin(x) * cos(y) + sin(y) * cos(z) + sin(z) * cos(x)


def schwarzP(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Primitive Schwarz surface."""
    return cos(x) + cos(y) + cos(z)


def schwarzD(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Diamond Schwarz surface."""
    a = sin(x) * sin(y) * sin(z)
    b = sin(x) * cos(y) * cos(z)
    c = cos(x) * sin(y) * cos(z)
    d = cos(x) * cos(y) * sin(z)
    return a + b + c + d


def neovius(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Neovius surface."""
    a = 3 * cos(x) + cos(y) + cos(z)
    b = 4 * cos(x) * cos(y) * cos(z)

    return a + b


def schoenIWP(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Schoen's IWP surface."""
    a = 2 * (cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x))
    b = cos(2 * x) + cos(2 * y) + cos(2 * z)

    return a - b


def schoenFRD(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Schoen's FRD surface."""
    a = 4 * cos(x) * cos(y) * cos(z)
    b = cos(2 * x) * cos(2 * y) + cos(2 * y) * cos(2 * z) + cos(2 * z) * cos(2 * x)
    return a - b


def fischerKochS(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Fischer-Koch surface."""
    a = cos(2 * x) * sin(y) * cos(z)
    b = cos(x) * cos(2 * y) * sin(z)
    c = sin(x) * cos(y) * cos(2 * z)

    return a + b + c


def pmy(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Primitive My surface."""
    a = 2 * cos(x) * cos(y) * cos(z)
    b = sin(2 * x) * sin(y)
    c = sin(x) * sin(2 * z)
    d = sin(2 * y) * sin(z)

    return a + b + c + d


def honeycomb(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Honeycomb surface."""
    return sin(x) * cos(y + pi / 2.0) + sin(y + pi / 2.0) + cos(z)


def lidinoid(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Lidinoid surface."""
    return (
        0.5
        * (
            sin(2 * x) * cos(y) * sin(z)
            + sin(2 * y) * cos(z) * sin(x)
            + sin(2 * z) * cos(x) * sin(y)
        )
        - 0.5
        * (cos(2 * x) * cos(2 * y) + cos(2 * y) * cos(2 * z) + cos(2 * z) * cos(2 * x))
        + 0.3
    )


def split_p(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Split P surface."""
    return (
        1.1
        * (
            sin(2 * x) * cos(y) * sin(z)
            + sin(2 * y) * cos(z) * sin(x)
            + sin(2 * z) * cos(x) * sin(y)
        )
        - 0.2
        * (cos(2 * x) * cos(2 * y) + cos(2 * y) * cos(2 * z) + cos(2 * z) * cos(2 * x))
        - 0.4 * (cos(2 * x) + cos(2 * y) + cos(2 * z))
    )


def honeycomb_gyroid(x: np.ndarray, y: np.ndarray, _: np.ndarray) -> np.ndarray:
    """Honeycomb gyroid surface."""
    return sin(x) * cos(y) + sin(y) + cos(x)


def honeycomb_primitive(x: np.ndarray, y: np.ndarray, _: np.ndarray) -> np.ndarray:
    """Honeycomb primitive surface."""
    return cos(x) + cos(y)


def honeycomb_diamond(x: np.ndarray, y: np.ndarray, _: np.ndarray) -> np.ndarray:
    """Honeycomb diamond surface."""
    return cos(x) * cos(y) + sin(x) * sin(y) + sin(x) * cos(y) + cos(x) * sin(y)


def honeycomb_I(x: np.ndarray, y: np.ndarray, _: np.ndarray) -> np.ndarray:
    """Honeycomb I surface."""
    return cos(x) * cos(y) + cos(y) + cos(x)


def honeycomb_L(x: np.ndarray, y: np.ndarray, _: np.ndarray) -> np.ndarray:
    """Honeycomb L surface."""
    return 1.1 * (sin(2 * x) * cos(y) + sin(2 * y) * sin(x) + cos(x) * sin(y)) - (
        cos(2 * x) * cos(2 * y) + cos(2 * y) + cos(2 * x)
    )


def SC(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Schwarz's surface."""
    return (
        2 * (cos(x) + cos(y) + cos(z))
        + cos(x) * cos(y)
        + cos(y) * cos(z)
        + cos(z) * cos(x)
    )


def I(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """I surface."""
    return cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x)


def P(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """P surface."""
    return sin(x) + sin(y) + sin(z)


def P_W(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """P_W surface."""
    a = 4 * (cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x))
    b = 3 * cos(x) * cos(y) * cos(z)
    return a - b


def double_gyroid(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Double gyroid surface."""
    return 2.75 * (
        sin(2 * x) * sin(z) * cos(y)
        + sin(2 * y) * sin(x) * cos(z)
        + sin(2 * z) * sin(y) * cos(x)
    ) - (cos(2 * x) * cos(2 * y) + cos(2 * y) * cos(2 * z) + cos(2 * z) * cos(2 * x))


def Gprime(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """G' surface."""
    return (
        5
        * (
            sin(2 * x) * sin(z) * cos(y)
            + sin(2 * y) * sin(x) * cos(z)
            + sin(2 * z) * sin(y) * cos(x)
        )
        + cos(2 * x) * cos(2 * y)
        + cos(2 * y) * cos(2 * z)
        + cos(2 * z) * cos(2 * x)
    )


def double_diamond(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Double diamond surface."""
    return (
        sin(2 * x) * sin(2 * y)
        + sin(2 * y) * sin(2 * z)
        + sin(2 * x) * sin(2 * z)
        + cos(2 * x) * cos(2 * y) * cos(2 * z)
    )


def Dprime(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """D' surface."""
    return (
        sin(x) * sin(y) * sin(z)
        + cos(x) * cos(y) * cos(z)
        - (cos(2 * x) * cos(2 * y) + cos(2 * y) * cos(2 * z) + cos(2 * z) * cos(2 * x))
        - 0.4
    )


def doubleP(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Double P surface."""
    return 0.5 * (cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x)) + 0.2 * (
        cos(2 * x) + cos(2 * y) + cos(2 * z)
    )


def OCTO(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Octo surface."""
    return (
        4 * (cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x))
        - 2.8 * cos(x) * cos(y) * cos(z)
        + (cos(x) + cos(y) + cos(z))
        + 1.5
    )


def PN(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """PN surface."""
    return (
        0.6 * (cos(x) * cos(y) * cos(z))
        + 0.4 * (cos(x) + cos(y) + cos(z))
        + 0.2 * (cos(2 * x) * cos(2 * y) * cos(2 * z))
        + 0.2 * (cos(2 * x) + cos(2 * y) + cos(2 * z))
        + 0.1 * (cos(3 * x) + cos(3 * y) + cos(3 * z))
        + 0.2 * (cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x))
    )


def KP(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """KP surface."""
    return (
        0.6 * (cos(x) + cos(y) + cos(z))
        + 0.7 * (cos(x) * cos(y) + cos(y) * cos(z) + cos(z) * cos(x))
        - 0.9 * (cos(2 * x) * cos(2 * y) * cos(2 * z))
        + 0.4
    )


def FRD(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """FRD surface."""
    return (
        8 * cos(x) * cos(y) * cos(z)
        + cos(2 * x) * cos(2 * y) * cos(2 * z)
        - cos(2 * x) * cos(2 * y)
        + cos(2 * y) * cos(2 * z)
        + cos(2 * z) * cos(2 * x)
    )


def splitP(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Split P surface."""
    return (
        1.1
        * (
            sin(2 * x) * sin(z) * cos(y)
            + sin(2 * y) * sin(x) * cos(z)
            + sin(2 * z) * sin(y) * cos(x)
        )
        - 0.2
        * (cos(2 * x) * cos(2 * y) + cos(2 * y) * cos(2 * z) + cos(2 * z) * cos(2 * x))
        - 0.4 * (cos(x) + cos(y) + cos(z))
    )
