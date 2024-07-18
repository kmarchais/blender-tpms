from inspect import getmembers, isfunction
from typing import Callable

import numpy as np
import pytest
from blender_tpms.tpms import surfaces


@pytest.mark.parametrize(
    "surface_function",
    [func[1] for func in getmembers(surfaces, isfunction)],
)
def test_surfaces(surface_function: Callable) -> None:
    """Test all TPMS surfaces."""
    assert -np.inf < surface_function(0, 0, 0) < np.inf
