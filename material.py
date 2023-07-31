import bpy

import numpy as np
import matplotlib.pyplot as plt

def apply_material(mesh, tpms, attr_name, colormap, n_colors):
    if bpy.context.space_data.shading.type not in ["MATERIAL", "RENDERED"]:
        bpy.context.space_data.shading.type = "MATERIAL"

    if attr_name not in bpy.data.materials:
        material = bpy.data.materials.new(name=attr_name)
    material = bpy.data.materials[attr_name]
    material.use_nodes = True

    bsdf = material.node_tree.nodes["Principled BSDF"]
    material_output_node = material.node_tree.nodes["Material Output"]

    attribute_node = material.node_tree.nodes.new("ShaderNodeAttribute")
    attribute_node.attribute_name = attr_name

    map_range_node = material.node_tree.nodes.new("ShaderNodeMapRange")
    map_range_node.inputs["From Min"].default_value = np.min(tpms.vtk_mesh[attr_name])
    map_range_node.inputs["From Max"].default_value = np.max(tpms.vtk_mesh[attr_name])

    color_ramp_node = material.node_tree.nodes.new("ShaderNodeValToRGB")

    # remove to create it again in the last iteration to have it selected
    last_elem = color_ramp_node.color_ramp.elements[-1]
    color_ramp_node.color_ramp.elements.remove(last_elem)

    cmap = plt.get_cmap(colormap)
    for i in range(n_colors):
        location = i / (n_colors - 1)
        if i != 0:
            color_ramp_node.color_ramp.elements.new(location)
        color = [c**2.2 for c in cmap(location)] # sRGB to Linear RGB
        color_ramp_node.color_ramp.elements[i].color = color

    color_ramp_node.select = False
    color_ramp_node.location = (bsdf.location.x - color_ramp_node.width - 50,
                                bsdf.location.y)
    color_ramp_node.label = colormap

    bsdf.select = False

    attribute_node.select = False
    map_range_node.select = False

    map_range_node.location = (color_ramp_node.location.x - map_range_node.width - 50,
                                    bsdf.location.y)
    attribute_node.location = (map_range_node.location.x - attribute_node.width - 50,
                                    bsdf.location.y)

    material.node_tree.links.new(attribute_node.outputs["Fac"], map_range_node.inputs["Value"])

    material.node_tree.links.new(map_range_node.outputs["Result"], color_ramp_node.inputs["Fac"])
    material.node_tree.links.new(color_ramp_node.outputs["Color"], bsdf.inputs["Base Color"])
    material.node_tree.links.new(bsdf.outputs["BSDF"], material_output_node.inputs["Surface"])

    bpy.data.objects[mesh.name].data.materials.append(material)
