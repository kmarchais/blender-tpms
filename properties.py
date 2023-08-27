from inspect import getmembers, isfunction
import itertools

import bpy

from bpy.props import (
    FloatProperty,
    EnumProperty,
    IntVectorProperty,
    FloatVectorProperty,
    IntProperty,
    StringProperty,
    BoolProperty,
)

from . import surfaces


functions = getmembers(surfaces, isfunction)
list_tpms = [(func[0], func[0], func[0]) for func in functions]

class OperatorProperties(bpy.types.PropertyGroup):
    auto_smooth: BoolProperty(
        name="Auto Smooth",
        description="Auto smooth",
        default=True,
        options={'SKIP_SAVE'},
    )

    material: BoolProperty(
        name="Apply Material",
        description="Apply material",
        default=False,
        options={'SKIP_SAVE'},
    )

class TpmsProperties(bpy.types.PropertyGroup):
    part: EnumProperty(
        items=[
            ("sheet", "Sheet", "Sheet"),
            ("lower_skeletal", "Lower Skeletal", "Lower Skeletal"),
            ("upper_skeletal", "Upper Skeletal", "Upper Skeletal"),
            ("skeletals", "Skeletals", "Skeletals"),
            ("surface", "Surface", "Surface"),
        ],
        name="Part",
        description="Part of the TPMS to generate",
        options={'SKIP_SAVE'},
    )

    cell_size: FloatVectorProperty(
        name="Cell size",
        subtype="XYZ",
        description="Dimensions of a unit cell",
        default=(1, 1, 1),
        min=0,
        options={'ANIMATABLE', 'SKIP_SAVE'},
    )

    repeat_cell: IntVectorProperty(
        name="Cell repetition",
        subtype="XYZ",
        description="Number of repetitions of a cell in each direction",
        default=(1, 1, 1),
        min=1,
        options={'ANIMATABLE', 'SKIP_SAVE'},
    )

    surface: EnumProperty(
        items=list_tpms,
        name="Surface",
        description="Tpms surface",
        default="gyroid",
        options={'SKIP_SAVE'},
    )

    swap: EnumProperty(
        name="Swap axes",
        description="Swap axes",
        default="XYZ",
        items=[
            3 * ("".join(xyz),) for xyz in itertools.permutations("XYZ")
        ],
        options={'SKIP_SAVE'},
    )

    offset: FloatProperty(
        name="Offset",
        description="Thickness of TPMS",
        default=0.3,
        min=0.01,
        options={'ANIMATABLE', 'SKIP_SAVE'},
    )

    phase_shift: FloatVectorProperty(
        name="Phase shift",
        subtype="XYZ",
        description="x = x + phi_x, y = y + phi_y, z = z + phi_z",
        default=(0, 0, 0),
        options={'ANIMATABLE', 'SKIP_SAVE'},
    )

    resolution: IntProperty(
        name="Resolution",
        description="Resolution of one unit cell",
        default=10,
        soft_max=50,
        min=10,
        options={'ANIMATABLE', 'SKIP_SAVE'},
    )

    density: StringProperty(
        name="Relative density",
        description="Relative density of the geometry",
    )


class CylindricalTpmsProperties(bpy.types.PropertyGroup):
    radius: FloatProperty(
        name="Radius",
        description="Radius of the cylinder",
        default=1,
        min=0.5,
        options={'ANIMATABLE', 'SKIP_SAVE'},
    )


# class TpmsGradingProperties(bpy.types.PropertyGroup):
#     surface_grading: StringProperty(
#         name="Surface grading",
#         description="Surface grading",
#         default="sin(x) * cos(y) + sin(y) * cos(z) + sin(z) * cos(x)",
#     )

#     offset_grading: StringProperty(
#         name="Offset grading",
#         description="Offset grading",
#         default="(b - a) * x + (a + b) / 2",
#     )

#     edges: FloatVectorProperty(
#         name="Edges (a, b)",
#         description="Min (a) and max (b) offset values",
#         size=2,
#         default=(0.3, 1.5),
#         min=0.01,
#         options={'ANIMATABLE'},
#     )
