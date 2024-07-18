import blender_tpms.tpms
import bpy
from blender_tpms.interface import polydata_to_mesh
from blender_tpms.ui import apply_material, set_shade_auto_smooth


def test_auto_smooth() -> None:
    tpms = blender_tpms.tpms.Tpms()
    mesh = polydata_to_mesh(tpms.sheet, mesh_name="Tpms")

    obj = bpy.data.objects.new(mesh.name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(state=True)

    assert mesh.name == "Tpms"
    set_shade_auto_smooth()


def test_apply_material() -> None:
    tpms = blender_tpms.tpms.Tpms()
    mesh = polydata_to_mesh(tpms.sheet, mesh_name="Tpms")

    obj = bpy.data.objects.new(mesh.name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(state=True)

    apply_material(
        mesh=mesh,
        tpms=tpms,
        attr_name="surface",
        colormap="coolwarm",
        n_colors=9,
    )
