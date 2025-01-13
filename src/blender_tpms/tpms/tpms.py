"""TPMS geometry generation."""

from __future__ import annotations

import itertools
from typing import Callable, Sequence

import numpy as np
import pyvista as pv

from blender_tpms.tpms import surfaces

Field = Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]

_3D = 3


class Tpms:
    """Triply periodic minimal surface geometry."""

    def __init__(
        self,
        part: str = "sheet",
        surface: str = "gyroid",
        swap: str = "XYZ",
        cell_size: float | Sequence[float] | np.ndarray = 1.0,
        repeat_cell: int | Sequence[int] | np.ndarray = 1,
        resolution: int = 20,
        offset: float | Field = 0.0,
        phase_shift: float | Sequence[float] | np.ndarray = (0.0, 0.0, 0.0),
    ) -> None:
        """Create a TPMS geometry."""
        if swap not in map("".join, itertools.permutations("XYZ")):
            err_msg = "swap must be a permutation of 'XYZ'"
            raise ValueError(err_msg)

        self._init_cell_parameters(cell_size, repeat_cell)

        self.part = part
        self.surface_function = getattr(surfaces, surface)
        self.swap = swap

        self.resolution = resolution
        self.offset = offset
        self.phase_shift = np.array(phase_shift)

        self.grid: pv.StructuredGrid
        self._vtk_mesh = None
        self._relative_density = None
        self._sheet = None
        self._lower_skeletal = None
        self._upper_skeletal = None
        self._surface = None
        self._skeletals = None

        self._compute_tpms_field()

    def _init_cell_parameters(
        self,
        cell_size: float | Sequence[float] | np.ndarray,
        repeat_cell: int | Sequence[int] | np.ndarray,
    ) -> None:
        """Initialize the cell size and the number of repetitions of the cell."""
        if isinstance(cell_size, (float, int)):
            self.cell_size = np.array([cell_size, cell_size, cell_size])
        elif len(cell_size) == _3D:
            self.cell_size = np.array(cell_size)
        else:
            err_msg = "cell_size must be a float or a sequence of 3 floats"
            raise ValueError(err_msg)

        if isinstance(repeat_cell, int):
            self.repeat_cell = np.array([repeat_cell, repeat_cell, repeat_cell])
        elif len(repeat_cell) == _3D:
            self.repeat_cell = np.array(repeat_cell)
        else:
            err_msg = "repeat_cell must be an int or a sequence of 3 ints"
            raise ValueError(err_msg)

    def vtk_sheet(self) -> pv.UnstructuredGrid:
        """Sheet surface of the TPMS geometry."""
        return self.grid.clip_scalar(scalars="upper_surface").clip_scalar(
            scalars="lower_surface",
            invert=False,
        )

    def vtk_upper_skeletal(self) -> pv.UnstructuredGrid:
        """Upper skeletal surface of the TPMS geometry."""
        return self.grid.clip_scalar(scalars="upper_surface", invert=False)

    def vtk_lower_skeletal(self) -> pv.UnstructuredGrid:
        """Lower skeletal surface of the TPMS geometry."""
        return self.grid.clip_scalar(scalars="lower_surface")

    @property
    def sheet(self) -> pv.PolyData:
        """Sheet surface of the TPMS geometry."""
        if self._sheet is not None:
            return self._sheet
        self._sheet = self.vtk_sheet().extract_surface().clean().triangulate()
        return self._sheet

    @property
    def lower_skeletal(self) -> pv.PolyData:
        """Lower skeletal surface of the TPMS geometry."""
        if self._lower_skeletal is not None:
            return self._lower_skeletal
        self._lower_skeletal = (
            self.vtk_lower_skeletal().extract_surface().clean().triangulate()
        )
        return self._lower_skeletal

    @property
    def upper_skeletal(self) -> pv.PolyData:
        """Upper skeletal surface of the TPMS geometry."""
        if self._upper_skeletal is not None:
            return self._upper_skeletal
        self._upper_skeletal = (
            self.vtk_upper_skeletal().extract_surface().clean().triangulate()
        )
        return self._upper_skeletal

    @property
    def skeletals(self) -> tuple[pv.PolyData, pv.PolyData]:
        """Lower and upper skeletal surfaces of the TPMS geometry."""
        if self._skeletals is not None:
            return self._skeletals
        self._skeletals = self.lower_skeletal + self.upper_skeletal
        return self._skeletals

    @property
    def surface(self) -> pv.PolyData:
        """Surface of the TPMS geometry."""
        if self._surface is not None:
            return self._surface
        self._surface = self.grid.contour(
            isosurfaces=[0.0],
            scalars="surface",
        ).extract_surface()
        return self._surface

    @property
    def vtk_mesh(self) -> pv.PolyData:
        """VTK mesh of the TPMS geometry."""
        if self._vtk_mesh is not None:
            return self._vtk_mesh

        self._compute_tpms_field()

        return getattr(self, self.part)

    @property
    def relative_density(self) -> float:
        """Relative density of the geometry."""
        if self._relative_density is not None:
            return self._relative_density
        grid_volume = np.prod(self.cell_size) * np.prod(self.repeat_cell)
        self._relative_density = self.vtk_mesh.volume / grid_volume
        return self._relative_density

    def _create_grid(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> pv.StructuredGrid:
        return pv.StructuredGrid(x, y, z)

    def _compute_tpms_field(self) -> None:
        linspaces = [
            np.linspace(
                -0.5 * cell_size_axis * repeat_cell_axis,
                0.5 * cell_size_axis * repeat_cell_axis,
                self.resolution * repeat_cell_axis,
            )
            for repeat_cell_axis, cell_size_axis in zip(
                self.repeat_cell,
                self.cell_size,
            )
        ]

        x, y, z = np.meshgrid(*linspaces)

        self.grid = self._create_grid(x, y, z)

        k_x, k_y, k_z = 2.0 * np.pi / self.cell_size
        xyz = {
            "X": k_x * (x + self.phase_shift[0]),
            "Y": k_y * (y + self.phase_shift[1]),
            "Z": k_z * (z + self.phase_shift[2]),
        }
        tpms_field = self.surface_function(*(xyz[axis] for axis in self.swap))

        self.grid["surface"] = tpms_field.ravel(order="F")
        self._update_offset(self.offset)

    def _update_offset(self, offset: float | Callable) -> None:
        if isinstance(offset, float):
            self.offset = offset
        elif isinstance(offset, Callable):
            self.offset = offset(self.grid.x, self.grid.y, self.grid.z).ravel("F")

        self.grid["lower_surface"] = self.grid["surface"] + 0.5 * self.offset
        self.grid["upper_surface"] = self.grid["surface"] - 0.5 * self.offset


class CylindricalTpms(Tpms):
    """Cylindrical TPMS geometry."""

    def __init__(
        self,
        radius: float = 1.0,
        cell_size: float | Sequence[float] | np.ndarray = 1.0,
        repeat_cell: int | Sequence[int] | np.ndarray = 1,
        **kwargs,
    ) -> None:
        """Create a cylindrical TPMS geometry."""
        self._init_cell_parameters(cell_size, repeat_cell)

        self.cylinder_radius = radius

        unit_theta = self.cell_size[1] / radius
        n_repeat_to_full_circle = int(round(2 * np.pi / unit_theta))
        self.unit_theta = 2 * np.pi / n_repeat_to_full_circle
        if self.repeat_cell[1] == 0 or self.repeat_cell[1] > n_repeat_to_full_circle:
            self.repeat_cell[1] = n_repeat_to_full_circle

        super().__init__(
            cell_size=self.cell_size,
            repeat_cell=self.repeat_cell,
            **kwargs,
        )

    @property
    def relative_density(self) -> float:
        """Relative density of the geometry."""
        if self._relative_density is not None:
            return self._relative_density
        grid_volume = (
            self.cylinder_radius
            * self.cell_size[0]
            * self.unit_theta
            * self.cell_size[2]
            * np.prod(self.repeat_cell)
        )
        self._relative_density = self.vtk_mesh.volume / grid_volume
        return self._relative_density

    def _create_grid(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> pv.StructuredGrid:
        rho = x + self.cylinder_radius
        theta = y * self.unit_theta

        return pv.StructuredGrid(rho * np.cos(theta), rho * np.sin(theta), z)


class CylindricalTwistedTpms(Tpms):
    """Cylindrical TPMS geometry with a twist."""

    def __init__(
        self,
        radius: float = 1.0,
        cell_size: float | Sequence[float] | np.ndarray = 1.0,
        repeat_cell: int | Sequence[int] | np.ndarray = 1,
        twist_rate: float = 0.0,  # New parameter for twist rate
        **kwargs,
    ) -> None:
        """Create a cylindrical TPMS geometry with a twist."""
        self._init_cell_parameters(cell_size, repeat_cell)

        self.cylinder_radius = radius
        self.twist_rate = twist_rate  # Store the twist rate

        unit_theta = self.cell_size[1] / radius
        n_repeat_to_full_circle = int(round(2 * np.pi / unit_theta))
        self.unit_theta = 2 * np.pi / n_repeat_to_full_circle
        if self.repeat_cell[1] == 0 or self.repeat_cell[1] > n_repeat_to_full_circle:
            self.repeat_cell[1] = n_repeat_to_full_circle

        super().__init__(
            cell_size=self.cell_size,
            repeat_cell=self.repeat_cell,
            **kwargs,
        )

    @property
    def relative_density(self) -> float:
        """Relative density of the geometry."""
        if self._relative_density is not None:
            return self._relative_density
        grid_volume = (
            self.cylinder_radius
            * self.cell_size[0]
            * self.unit_theta
            * self.cell_size[2]
            * np.prod(self.repeat_cell)
        )
        self._relative_density = self.vtk_mesh.volume / grid_volume
        return self._relative_density

    def _create_grid(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> pv.StructuredGrid:
        """Create a grid with a twist effect."""
        rho = x + self.cylinder_radius
        theta = y * self.unit_theta + self.twist_rate * z  # Add twist based on z
        return pv.StructuredGrid(rho * np.cos(theta), rho * np.sin(theta), z)


class SphericalTpms(Tpms):
    """Spherical TPMS geometry."""

    def __init__(
        self,
        radius: float = 1.0,
        cell_size: float | Sequence[float] | np.ndarray = 1.0,
        repeat_cell: int | Sequence[int] | np.ndarray = 1,
        **kwargs,
    ) -> None:
        """Create a spherical TPMS geometry."""
        self._init_cell_parameters(cell_size, repeat_cell)

        self.sphere_radius = radius

        unit_theta = self.cell_size[1] / radius
        n_repeat_theta_to_join = int(np.pi / unit_theta)
        self.unit_theta = np.pi / n_repeat_theta_to_join
        if self.repeat_cell[1] == 0 or self.repeat_cell[1] > n_repeat_theta_to_join:
            self.repeat_cell[1] = n_repeat_theta_to_join

        unit_phi = self.cell_size[2] / radius
        n_repeat_phi_to_join = int(2 * np.pi / unit_phi)
        self.unit_phi = 2 * np.pi / n_repeat_phi_to_join
        if self.repeat_cell[2] == 0 or self.repeat_cell[2] > n_repeat_phi_to_join:
            self.repeat_cell[2] = n_repeat_phi_to_join

        super().__init__(
            cell_size=self.cell_size,
            repeat_cell=self.repeat_cell,
            **kwargs,
        )

    @property
    def relative_density(self) -> float:
        """Relative density of the geometry."""
        if self._relative_density is not None:
            return self._relative_density
        self._relative_density = self.vtk_mesh.volume / abs(self.grid.volume)
        return self._relative_density

    def _create_grid(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> pv.StructuredGrid:
        rho = x + self.sphere_radius
        theta = y * self.unit_theta + np.pi / 2.0
        phi = z * self.unit_phi

        return pv.StructuredGrid(
            rho * np.sin(theta) * np.cos(phi),
            rho * np.sin(theta) * np.sin(phi),
            rho * np.cos(theta),
        )


# class GradedTpms(Tpms):
#     def __init__(
#         self,
#         part,
#         surface,
#         swap,
#         cell_size,
#         repeat_cell,
#         resolution,
#         offset,
#         phase_shift,
#         offset_grading,
#         edges,
#     ):
#         super().__init__(
#             part,
#             surface,
#             swap,
#             cell_size,
#             repeat_cell,
#             resolution,
#             offset,
#             phase_shift,
#         )
#         self.offset_grading = offset_grading
#         self.edges = edges


#     def _create_grid(self, x, y, z):
#         a = self.edges[0]
#         b = self.edges[1]
#         self.offset = literal_eval(self.offset_grading)
#         return pv.StructuredGrid(x, y, z)
