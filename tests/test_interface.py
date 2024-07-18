import pyvista as pv
from blender_tpms.interface import get_all_surfaces, polydata_to_mesh

# ruff: noqa: S101


def test_polydata_to_mesh() -> None:
    """Test polydata_to_mesh function."""
    polydata = pv.Cube()
    mesh = polydata_to_mesh(polydata, mesh_name="Box")
    assert mesh.name == "Box"
    assert len(mesh.vertices) == 8
    assert len(mesh.polygons) == 12


def test_get_all_surfaces() -> None:
    """Test get_all_surfaces function."""
    surfaces = get_all_surfaces()
    assert len(surfaces) == 30
    for surface in surfaces:
        assert len(surface) == 3
        assert isinstance(surface[0], str)
        assert isinstance(surface[1], str)
        assert isinstance(surface[2], str)
        assert surface[0] == surface[1] == surface[2]
