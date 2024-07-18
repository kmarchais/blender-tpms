"""Material module to visualize the TPMS field on the surface of the mesh."""

from __future__ import annotations

from typing import TYPE_CHECKING

import bpy
import matplotlib.pyplot as plt
import numpy as np

if TYPE_CHECKING:
    from blender_tpms.tpms.tpms import Tpms  # pragma: no cover


def shader_node_attribute(
    material: bpy.types.Material,
    attr_name: str,
) -> bpy.types.ShaderNodeAttribute:
    """Create an attribute node to get the TPMS field values."""
    attribute_node = material.node_tree.nodes.new("ShaderNodeAttribute")
    if not isinstance(attribute_node, bpy.types.ShaderNodeAttribute):
        raise TypeError("Shader node is not ShaderNodeAttribute")  # pragma: no cover

    attribute_node.attribute_name = attr_name
    return attribute_node


def shader_node_map_range(
    material: bpy.types.Material,
    attr_name: str,
    tpms: Tpms,
) -> bpy.types.ShaderNodeMapRange:
    """Create a map range node to map the attribute values to the color ramp."""
    map_range_node = material.node_tree.nodes.new("ShaderNodeMapRange")
    if not isinstance(map_range_node, bpy.types.ShaderNodeMapRange):
        raise TypeError("Shader node is not ShaderNodeMapRange")  # pragma: no cover

    map_range_node.inputs["From Min"].default_value = np.min(tpms.vtk_mesh[attr_name])
    map_range_node.inputs["From Max"].default_value = np.max(tpms.vtk_mesh[attr_name])
    return map_range_node


def shader_node_val_to_rgb(
    material: bpy.types.Material,
    colormap: str,
    n_colors: int,
) -> bpy.types.ShaderNodeValToRGB:
    """Create a color ramp node with a colormap."""
    color_ramp_node = material.node_tree.nodes.new("ShaderNodeValToRGB")

    if not isinstance(color_ramp_node, bpy.types.ShaderNodeValToRGB):
        raise TypeError("Shader node is not ShaderNodeVal")  # pragma: no cover

    # remove to create it again in the last iteration to have it selected
    last_elem = color_ramp_node.color_ramp.elements[-1]
    color_ramp_node.color_ramp.elements.remove(last_elem)

    cmap = plt.get_cmap(colormap)
    for i in range(n_colors):
        location = i / (n_colors - 1)
        if i != 0:
            color_ramp_node.color_ramp.elements.new(location)
        color = [c**2.2 for c in cmap(location)]  # sRGB to Linear RGB
        color_ramp_node.color_ramp.elements[i].color = color

    color_ramp_node.label = colormap
    return color_ramp_node


def link_nodes(
    material: bpy.types.Material,
    bsdf: bpy.types.Node,
    attribute_node: bpy.types.Node,
    map_range_node: bpy.types.Node,
    color_ramp_node: bpy.types.Node,
    material_output_node: bpy.types.Node,
) -> None:
    """Link the nodes to create the material."""
    material.node_tree.links.new(
        attribute_node.outputs["Fac"],
        map_range_node.inputs["Value"],
    )

    material.node_tree.links.new(
        map_range_node.outputs["Result"],
        color_ramp_node.inputs["Fac"],
    )
    material.node_tree.links.new(
        color_ramp_node.outputs["Color"],
        bsdf.inputs["Base Color"],
    )
    material.node_tree.links.new(
        bsdf.outputs["BSDF"],
        material_output_node.inputs["Surface"],
    )


def move_nodes(
    bsdf: bpy.types.Node,
    attribute_node: bpy.types.Node,
    map_range_node: bpy.types.Node,
    color_ramp_node: bpy.types.Node,
) -> None:
    """Move the nodes so they are not on top of each other."""
    bsdf.select = False
    color_ramp_node.select = False
    attribute_node.select = False
    map_range_node.select = False

    color_ramp_node.location = (
        bsdf.location.x - color_ramp_node.width - 50,
        bsdf.location.y,
    )

    map_range_node.location = (
        color_ramp_node.location.x - map_range_node.width - 50,
        bsdf.location.y,
    )
    attribute_node.location = (
        map_range_node.location.x - attribute_node.width - 50,
        bsdf.location.y,
    )


def switch_to_material_shading() -> None:
    """Switch to material shading if not already in material or rendered mode."""
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if (
                    space.type == "VIEW_3D"
                    and isinstance(space, bpy.types.SpaceView3D)
                    and space.shading.type not in ["MATERIAL", "RENDERED"]
                ):
                    space.shading.type = "MATERIAL"
                    return


def create_material(attr_name: str) -> bpy.types.Material:
    """Create a new material or get the existing one and activate the nodes."""
    if attr_name not in bpy.data.materials:
        material = bpy.data.materials.new(name=attr_name)
    material = bpy.data.materials[attr_name]
    material.use_nodes = True
    return material


def apply_material(
    mesh: bpy.types.Mesh,
    tpms: Tpms,
    attr_name: str,
    colormap: str,
    n_colors: int,
) -> None:
    """Apply a material to the mesh based on the TPMS field."""
    switch_to_material_shading()

    material = create_material(attr_name)

    bsdf = material.node_tree.nodes["Principled BSDF"]
    attribute_node = shader_node_attribute(material, attr_name)
    map_range_node = shader_node_map_range(material, attr_name, tpms)
    color_ramp_node = shader_node_val_to_rgb(material, colormap, n_colors)
    material_output_node = material.node_tree.nodes["Material Output"]

    move_nodes(bsdf, attribute_node, map_range_node, color_ramp_node)

    link_nodes(
        material,
        bsdf,
        attribute_node,
        map_range_node,
        color_ramp_node,
        material_output_node,
    )

    bpy.data.objects[mesh.name].data.materials.append(material)
