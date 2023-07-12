import bpy
from bpy_extras.object_utils import AddObjectHelper

from bpy.props import (
    FloatProperty,
    EnumProperty,
    IntVectorProperty,
    FloatVectorProperty,
    IntProperty,
    StringProperty,
)

def install_dependencies():
    import sys, subprocess
    for dependency in dependencies.keys():
        if dependency != 'pip':
            subprocess.call([sys.executable, "-m", "pip", "install", *dependencies])

dependencies = {'pip': {},
                'pyvista': {"url": "https://github.com/pyvista/pyvista"},}
install_dependencies()

import pyvista as pv
from numpy import pi
import numpy as np

from . import tpms

bl_info = {
    "name": "TPMS",
    "author": "kmarchais",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "location": "Add > TPMS",
    "description": "Create a TPMS mesh",
    "warning": "",
    "doc_url": "https://github.com/kmarchais/blender-tpms",
    "category": "Add Mesh",
}

list_tpms = [ # (identifier, name, description)
    ("gyroid", "Gyroid", "Schoen Gyroid"),
    ("schwarzP", "Schwarz P", "Schwarz Primitive"),
    ("schwarzD", "Schwarz D", "Schwarz Diamond"),
    ("neovius", "Neovius", "Neovius"),
    ("schoenIWP", "Schoen I-WP", "Schoen I-WP"),
    ("schoenFRD", "Schoen F-RD", "Schoen F-RD"),
    ("fischerKochS", "Fischer Koch S", "Fischer Koch S"),
    ("pmy", "PMY", "PMY"),
    ("honeycomb", "Honeycomb", "Honeycomb"),
    ("lidinoid", "Lidinoid", "Lidinoid"),
    ("split_p", "Split P", "Split P"),
    # ("gyroid_honeycomb", "Gyroid Honeycomb", "Gyroid Honeycomb"),
    # ("primitive_honeycomb", "Primitive Honeycomb", "Primitive Honeycomb"),
]


def generate_tpms(tpms_type, cell_size, repeat_cell, resolution, offset):    
    repeat_cell = np.array(repeat_cell)
    cell_size = np.array(cell_size)

    linspaces = [
        np.linspace(
            -0.5 * cell_size[i] * repeat_cell[i],
            0.5 * cell_size[i] * repeat_cell[i],
            resolution * repeat_cell[i],
        )
        for i in range(3)
    ]

    x, y, z = np.meshgrid(*linspaces)
    k_x, k_y, k_z = 2. * pi / cell_size

    surface_function = getattr(tpms, tpms_type)(k_x * x, k_y * y, k_z * z)

    grid = pv.StructuredGrid(x, y, z)
    grid["surface"] = surface_function.ravel(order='F')
    grid["lower_surface"] = (surface_function - 0.5 * offset).ravel(order='F')
    grid["upper_surface"] = (surface_function + 0.5 * offset).ravel(order='F')

    return grid.clip_scalar(scalars="upper_surface", invert=False).clip_scalar(scalars="lower_surface").extract_geometry()


class Tpms(bpy.types.Operator, AddObjectHelper):
    """Add a TPMS mesh"""
    bl_idname = "mesh.tpms_add"
    bl_label = "TPMS"
    bl_options = {'REGISTER', 'UNDO'}

    tpms_type: EnumProperty(
        items=list_tpms,
        name="Type",
        description="Tpms type",
    )

    cell_size: FloatVectorProperty(
        name="Cell size",
        description="Dimensions of a unit cell",
        default=(1, 1, 1),
        min=0,
    )

    repeat_cell: IntVectorProperty(
        name="Cell repetition",
        description="Number of repetitions of a cell in each direction",
        default=(1, 1, 1),
        min=1,
    )

    resolution: IntProperty(
        name="Resolution",
        description="Resolution of one unit cell",
        default=10,
        soft_max=50,
        min=10,
    )

    offset: FloatProperty(
        name="Offset",
        description="Thickness of TPMS",
        default=0.3,
        min=0.01,
    )

    density: StringProperty(
        name="Relative density",
        description="Relative density of the geometry",
    )

    def execute(self, context):
        polydata = generate_tpms(self.tpms_type, self.cell_size, self.repeat_cell, self.resolution, self.offset)

        faces = []
        if not polydata.is_all_triangles:
            polydata = polydata.triangulate()
        faces = np.reshape(polydata.faces, (polydata.n_faces, 4))[:, 1:]

        mesh = bpy.data.meshes.new("Tpms")
        mesh.from_pydata(vertices=polydata.points, edges=[], faces=faces)
        mesh.update()

        box_volume = self.cell_size[0] * self.cell_size[1] * self.cell_size[2] * self.repeat_cell[0] * self.repeat_cell[1] * self.repeat_cell[2]
        relative_density = polydata.volume / box_volume
        self.density = f"{relative_density:.1%}"

        attr_name = "surface"
        if attr_name not in mesh.attributes.keys():
            mesh.attributes.new(attr_name, type='FLOAT', domain='POINT')
        mesh.attributes[attr_name].data.foreach_set('value', polydata[attr_name])

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(Tpms.bl_idname, icon='MESH_CUBE')


def register():
    bpy.utils.register_class(Tpms)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(Tpms)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
