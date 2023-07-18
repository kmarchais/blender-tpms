import numpy as np
from numpy import pi
import pyvista as pv

from . import surfaces

class Tpms:
    def __init__(self, part, surface, cell_size, repeat_cell, resolution, offset, phase_shift):
        self.part = part
        self.surface_function = getattr(surfaces, surface)
        self.repeat_cell = np.array(repeat_cell)
        self.cell_size = np.array(cell_size)
        self.resolution = resolution
        self.offset = offset
        self.phase_shift = np.array(phase_shift)

        self.grid = None
        self._vtk_mesh = None
        self._relative_density = None
        self._sheet = None
        self._lower_skeletal = None
        self._upper_skeletal = None
        self._skeletals = None
        self._surface = None

    @property
    def sheet(self):
        if self._sheet is not None:
            return self._sheet
        self._sheet = (
            self.grid
            .clip_scalar(scalars="upper_surface", invert=False)
            .clip_scalar(scalars="lower_surface")
            .extract_surface()
        )
        return self._sheet

    @property
    def lower_skeletal(self):
        if self._lower_skeletal is not None:
            return self._lower_skeletal
        self._lower_skeletal = (
            self.grid
            .clip_scalar(scalars="lower_surface", invert=False)
            .extract_surface()
        )
        return self._lower_skeletal

    @property
    def upper_skeletal(self):
        if self._upper_skeletal is not None:
            return self._upper_skeletal
        self._upper_skeletal = (
            self.grid
            .clip_scalar(scalars="upper_surface")
            .extract_surface()
        )
        return self._upper_skeletal

    @property
    def skeletals(self):
        if self._skeletals is not None:
            return self._skeletals
        self._skeletals = self.lower_skeletal.merge(self.upper_skeletal)
        return self._skeletals

    @property
    def surface(self):
        if self._surface is not None:
            return self._surface
        self._surface = (
            self.grid
            .contour(isosurfaces=[0.0], scalars="surface")
            .extract_surface()
        )
        return self._surface

    @property
    def vtk_mesh(self):
        if self._vtk_mesh is not None:
            return self._vtk_mesh

        self._compute_tpms_field()

        return getattr(self, self.part)

    @property
    def relative_density(self):
        if self._relative_density is not None:
            return self._relative_density
        grid_volume = np.prod(self.cell_size) * np.prod(self.repeat_cell)
        self._relative_density = self.vtk_mesh.volume / grid_volume
        return self._relative_density

    def _create_grid(self, x, y, z):
        return pv.StructuredGrid(x, y, z)

    def _compute_tpms_field(self):
        linspaces = [
            np.linspace(
                -0.5 * cell_size_axis * repeat_cell_axis,
                0.5 * cell_size_axis * repeat_cell_axis,
                self.resolution * repeat_cell_axis,
            )
            for repeat_cell_axis, cell_size_axis in zip(
                self.repeat_cell, self.cell_size
            )
        ]

        x, y, z = np.meshgrid(*linspaces)

        self.grid = self._create_grid(x, y, z)

        k_x, k_y, k_z = 2.0 * np.pi / self.cell_size
        surface_function = self.surface_function(
            k_x * (x + self.phase_shift[0]),
            k_y * (y + self.phase_shift[1]),
            k_z * (z + self.phase_shift[2]),
        )

        self.grid["surface"] = surface_function.ravel(order="F")
        self.grid["lower_surface"] = (surface_function - 0.5 * self.offset).ravel(order="F")
        self.grid["upper_surface"] = (surface_function + 0.5 * self.offset).ravel(order="F")

class CylindricalTpms(Tpms):
    def __init__(self, radius, part, surface, cell_size, repeat_cell, resolution, offset, phase_shift):
        unit_theta = cell_size[1] / radius
        n_repeat_to_full_circle = int(round(2 * np.pi / unit_theta))
        unit_theta = 2 * np.pi / n_repeat_to_full_circle
        # cell_size[1] = unit_theta * radius # TODO : check if this is correct
        if repeat_cell[1] == 0 or repeat_cell[1] > n_repeat_to_full_circle:
            repeat_cell[1] = n_repeat_to_full_circle

        super().__init__(part, surface, cell_size, repeat_cell, resolution, offset, phase_shift)
        self.cylinder_radius = radius
        self.unit_theta = unit_theta

    @property
    def relative_density(self):
        if self._relative_density is not None:
            return self._relative_density
        grid_volume = 4.0 * self.cylinder_radius * self.cell_size[0] * self.unit_theta * self.cell_size[2] * np.prod(self.repeat_cell)
        self._relative_density = self.vtk_mesh.volume / grid_volume
        return self._relative_density

    def _create_grid(self, x, y, z):
        rho = x + self.cylinder_radius
        theta = y * self.unit_theta

        return pv.StructuredGrid(rho * np.cos(theta), rho * np.sin(theta), z)
