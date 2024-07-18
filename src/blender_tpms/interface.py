"""Interface between PyVista and Blender."""

from __future__ import annotations

from inspect import getmembers, isfunction
from typing import TYPE_CHECKING

import bpy
import numpy as np

if TYPE_CHECKING:
    import pyvista as pv  # pragma: no cover


def polydata_to_mesh(polydata: pv.PolyData, mesh_name: str = "Tpms") -> bpy.types.Mesh:
    """Convert a vtkPolyData to a mesh."""
    faces = []
    if not polydata.is_all_triangles:
        polydata = polydata.triangulate()
    polydata.flip_normals()
    faces = np.reshape(polydata.faces, (polydata.n_cells, 4))[:, 1:]

    mesh = bpy.data.meshes.new(mesh_name)
    mesh.from_pydata(vertices=polydata.points, edges=[], faces=faces)
    mesh.update()

    return mesh


def get_all_surfaces() -> list[tuple[str, str, str]]:
    """Get all TPMS surfaces."""
    from .tpms import surfaces

    functions = getmembers(surfaces, isfunction)
    return [(func[0], func[0], func[0]) for func in functions]
