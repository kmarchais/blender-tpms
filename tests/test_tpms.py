from blender_tpms.tpms import CylindricalTpms, SphericalTpms, Tpms


def test_tpms() -> None:
    tpms = Tpms()
    assert tpms is not None
    assert tpms.surface is not None
    assert tpms.sheet is not None
    assert tpms.lower_skeletal is not None
    assert tpms.upper_skeletal is not None
    assert tpms.skeletals is not None
    assert tpms.relative_density > 0
    assert tpms.vtk_sheet() is not None
    assert tpms.vtk_lower_skeletal() is not None
    assert tpms.vtk_upper_skeletal() is not None


def test_cylindrical_tpms() -> None:
    tpms = CylindricalTpms()

    assert tpms.relative_density > 0

def test_spherical_tpms() -> None:
    tpms = SphericalTpms()

    assert tpms.relative_density > 0


