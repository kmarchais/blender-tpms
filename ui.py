import bpy
import numpy as np
import pyvista as pv
from bpy_extras.object_utils import AddObjectHelper, object_data_add

from .material import apply_material

# GradedTpms,
from .properties import (
    CylindricalTpmsProperties,
    # TpmsGradingProperties,
    OperatorProperties,
    SphericalTpmsProperties,
    TpmsProperties,
)
from .tpms import (
    CylindricalTpms,
    SphericalTpms,
    Tpms,
)


def set_shade_auto_smooth() -> None:
    """Set the auto smooth shading to the active object."""
    # use kwargs for compatibility with blender > 4.1
    # `use_auto_smooth` is not a parameter of `shade_smooth` from blender 4.1
    kwargs = {"use_auto_smooth": True} if bpy.app.version < (4, 1) else {}
    bpy.ops.object.shade_smooth(**kwargs)


def polydata_to_mesh(polydata: pv.PolyData, mesh_name: str = "Tpms") -> bpy.types.Mesh:
    """Convert a vtkPolyData to a mesh."""
    faces = []
    if not polydata.is_all_triangles:
        polydata = polydata.triangulate()
    polydata.flip_normals()
    faces = np.reshape(polydata.faces, (polydata.n_faces, 4))[:, 1:]

    mesh = bpy.data.meshes.new(mesh_name)
    mesh.from_pydata(vertices=polydata.points, edges=[], faces=faces)
    mesh.update()

    return mesh


class OperatorTpms(
    bpy.types.Operator, OperatorProperties, AddObjectHelper, TpmsProperties
):
    """Add a TPMS mesh."""

    bl_idname = "mesh.tpms_add"
    bl_label = "TPMS"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context):
        tpms = Tpms(
            part=self.part,
            surface=self.surface,
            swap=self.swap,
            cell_size=self.cell_size,
            repeat_cell=self.repeat_cell,
            resolution=self.resolution,
            offset=self.offset,
            phase_shift=self.phase_shift,
        )

        mesh = polydata_to_mesh(tpms.vtk_mesh)

        self.density = f"{tpms.relative_density:.1%}"

        # add the mesh as an object into the scene with this utility module
        object_data_add(context, mesh, operator=self)

        attr_name = "surface"
        mesh.attributes.new(attr_name, type="FLOAT", domain="POINT")
        mesh.attributes[attr_name].data.foreach_set("value", tpms.vtk_mesh[attr_name])

        if self.auto_smooth:
            set_shade_auto_smooth()

        if self.material:
            apply_material(
                mesh=mesh,
                tpms=tpms,
                attr_name=attr_name,
                colormap="coolwarm",
                n_colors=9,
            )

        return {"FINISHED"}


class OperatorCylindricalTpms(
    bpy.types.Operator,
    OperatorProperties,
    AddObjectHelper,
    TpmsProperties,
    CylindricalTpmsProperties,
):
    """Add a Cylindrical TPMS mesh."""

    bl_idname = "mesh.cylindrical_tpms_add"
    bl_label = "Cylindrical TPMS"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context):
        tpms = CylindricalTpms(
            radius=self.radius,
            part=self.part,
            surface=self.surface,
            swap=self.swap,
            cell_size=self.cell_size,
            repeat_cell=self.repeat_cell,
            resolution=self.resolution,
            offset=self.offset,
            phase_shift=self.phase_shift,
        )

        mesh = polydata_to_mesh(tpms.vtk_mesh)

        self.density = f"{tpms.relative_density:.1%}"

        # add the mesh as an object into the scene with this utility module
        object_data_add(context, mesh, operator=self)

        attr_name = "surface"
        mesh.attributes.new(attr_name, type="FLOAT", domain="POINT")
        mesh.attributes[attr_name].data.foreach_set("value", tpms.vtk_mesh[attr_name])

        if self.auto_smooth:
            set_shade_auto_smooth()

        if self.material:
            apply_material(
                mesh=mesh,
                tpms=tpms,
                attr_name=attr_name,
                colormap="coolwarm",
                n_colors=9,
            )

        return {"FINISHED"}


class OperatorSphericalTpms(
    bpy.types.Operator,
    OperatorProperties,
    AddObjectHelper,
    TpmsProperties,
    SphericalTpmsProperties,
):
    """Add a Spherical TPMS mesh."""

    bl_idname = "mesh.spherical_tpms_add"
    bl_label = "Spherical TPMS"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context):
        tpms = SphericalTpms(
            radius=self.radius,
            part=self.part,
            surface=self.surface,
            swap=self.swap,
            cell_size=self.cell_size,
            repeat_cell=self.repeat_cell,
            resolution=self.resolution,
            offset=self.offset,
            phase_shift=self.phase_shift,
        )

        mesh = polydata_to_mesh(tpms.vtk_mesh)

        self.density = f"{tpms.relative_density:.1%}"

        # add the mesh as an object into the scene with this utility module
        object_data_add(context, mesh, operator=self)

        attr_name = "surface"
        mesh.attributes.new(attr_name, type="FLOAT", domain="POINT")
        mesh.attributes[attr_name].data.foreach_set("value", tpms.vtk_mesh[attr_name])

        if self.auto_smooth:
            set_shade_auto_smooth()

        if self.material:
            apply_material(
                mesh=mesh,
                tpms=tpms,
                attr_name=attr_name,
                colormap="coolwarm",
                n_colors=9,
            )

        return {"FINISHED"}


# class OperatorGradedTpms(
#     bpy.types.Operator,
#     OperatorProperties,
#     AddObjectHelper,
#     TpmsGradingProperties,
#     TpmsProperties,
# ):
#     """Add a Graded TPMS mesh"""

#     bl_idname = "mesh.graded_tpms_add"
#     bl_label = "Graded TPMS"
#     bl_options = {"REGISTER", "UNDO"}

#     def execute(self, context):
#         tpms = GradedTpms(
#             self.part,
#             self.surface,
#             self.swap,
#             self.cell_size,
#             self.repeat_cell,
#             self.resolution,
#             self.offset,
#             self.phase_shift,
#             self.offset_grading,
#             self.edges,
#         )

#         mesh = polydata_to_mesh(tpms.vtk_mesh)

#         self.density = f"{tpms.relative_density:.1%}"

#         # add the mesh as an object into the scene with this utility module
#         object_data_add(context, mesh, operator=self)

#         attr_name = "surface"
#         mesh.attributes.new(attr_name, type="FLOAT", domain="POINT")
#         mesh.attributes[attr_name].data.foreach_set("value", tpms.vtk_mesh[attr_name])

#         if self.auto_smooth:
#             set_shade_auto_smooth()


#         if self.material:
#             apply_material(mesh=mesh, tpms=tpms, attr_name=attr_name, colormap="coolwarm", n_colors=9)

#         return {'FINISHED'}


# class OperatorGradedCylindricalTpms(bpy.types.Operator, OperatorProperties, AddObjectHelper, TpmsGradingProperties, TpmsProperties, CylindricalTpmsProperties):
#     """Add a Graded Cylindrical TPMS mesh"""
#     bl_idname = "mesh.cylindrical_graded_tpms_add"
#     bl_label = "Graded Cylindrical TPMS"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self, context):
#         return {'FINISHED'}


def menu_func(self, context):
    # Create the main submenu
    self.layout.menu("OBJECT_MT_tpms_submenu", icon="MESH_CUBE")


class OBJECT_MT_tpms_submenu(bpy.types.Menu):
    bl_label = "TPMS"
    bl_idname = "OBJECT_MT_tpms_submenu"

    def draw(self, context):
        layout = self.layout
        layout.operator(OperatorTpms.bl_idname, icon="MESH_CUBE")
        layout.operator(OperatorCylindricalTpms.bl_idname, icon="MESH_CYLINDER")
        layout.operator(OperatorSphericalTpms.bl_idname, icon="MESH_UVSPHERE")
        # layout.operator(OperatorGradedTpms.bl_idname, icon='MESH_CUBE')
        # layout.operator(OperatorGradedCylindricalTpms.bl_idname, icon='MESH_CYLINDER')


def register():
    bpy.utils.register_class(OBJECT_MT_tpms_submenu)
    bpy.utils.register_class(OperatorTpms)
    bpy.utils.register_class(OperatorCylindricalTpms)
    bpy.utils.register_class(OperatorSphericalTpms)
    # bpy.utils.register_class(OperatorGradedTpms)
    # bpy.utils.register_class(OperatorGradedCylindricalTpms)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_MT_tpms_submenu)
    bpy.utils.unregister_class(OperatorTpms)
    bpy.utils.unregister_class(OperatorCylindricalTpms)
    bpy.utils.unregister_class(OperatorSphericalTpms)
    # bpy.utils.unregister_class(OperatorGradedTpms)
    # bpy.utils.unregister_class(OperatorGradedCylindricalTpms)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
