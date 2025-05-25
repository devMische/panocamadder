# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from . pca_funcs import cleanstr

# Add HotSpot Operator


class PCAPLUS_OT_addhsop(bpy.types.Operator):
    """Open the 'Add Hotspot' dialog box"""
    bl_label = "Add Hotspot"
    bl_idname = "pcaplus.addhsop"
    bl_options = {'UNDO'}

    hsname: bpy.props.StringProperty(
        name="Name: ", description="The hotspot name", default="My Hotspot")  # type: ignore
    hscolor: bpy.props.FloatVectorProperty(name="Color: ", description="The background-color",
                                           subtype="COLOR", size=3, min=0.0, max=1.0, default=(1.0, 1.0, 1.0))  # type: ignore

    def execute(self, context):

        hsn = self.hsname
        hsn = cleanstr(hsn)

        hsbgr = self.hscolor[0]
        hsbgg = self.hscolor[1]
        hsbgb = self.hscolor[2]

        # Add primitive_plane
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.mesh.primitive_plane_add(
            size=1.4, enter_editmode=False, align='CURSOR', scale=(1, 1, 1))

        # Scale to 0.5
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))
        bpy.context.object.show_bounds = True
        bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'

        bpy.context.object.name = hsn

        # Create Emission Material
        obj = bpy.context.active_object
        objname = bpy.context.active_object.name

        # remove all materials
        for s in obj.material_slots:
            bpy.ops.object.material_slot_remove()

        hsmat = bpy.data.materials.new(name="new")
        hsmat.use_nodes = True
        hsmat.name = objname + "_HSMAT"

        # alpha blend mode / viewportcolor
        hsmat.blend_method = 'BLEND'
        hsmat.diffuse_color = (hsbgr, hsbgg, hsbgb, 1.0)

        # Remove default material
        # title of the existing node when materials.new
        hsmat.node_tree.nodes.remove(
            hsmat.node_tree.nodes.get('Principled BSDF'))
        hsmat_output = hsmat.node_tree.nodes.get('Material Output')

        # add transparent shader
        transparent = hsmat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
        transparent.location = (-10, 380)
        transparent.inputs[0].default_value = (1, 1, 1, 1.0)

        # add emission shader
        emi = hsmat.node_tree.nodes.new('ShaderNodeEmission')
        emi.location = (-10, 280)

        # add mix shader
        mixer = hsmat.node_tree.nodes.new('ShaderNodeMixShader')
        mixer.name = 'pca-hsalpha-mixer'
        mixer.label = 'PCA Alpha Mixer'
        mixer.inputs[0].default_value = 1.0
        mixer.location = (145, 280)

        # add rgb shader
        color = hsmat.node_tree.nodes.new('ShaderNodeRGB')
        color.name = 'pca-hscolor'
        color.label = 'PCA Hotspot Color'
        color.outputs[0].default_value = (hsbgr, hsbgg, hsbgb, 1.0)
        color.location = (-500, -100)

        # add tex coord node
        texcord = hsmat.node_tree.nodes.new("ShaderNodeTexCoord")
        texcord.location = (-1400, 350)

        # add mapping node
        mappcord = hsmat.node_tree.nodes.new("ShaderNodeMapping")
        mappcord.location = (-1200, 180)
        mappcord.inputs[3].default_value[0] = 3
        mappcord.inputs[3].default_value[1] = 3
        mappcord.inputs[1].default_value[0] = -1.5
        mappcord.inputs[1].default_value[1] = -1.5

        # add seperate xyz node
        sepxyz = hsmat.node_tree.nodes.new("ShaderNodeSeparateXYZ")
        sepxyz.location = (-1200, 480)

        # add math node
        math = hsmat.node_tree.nodes.new("ShaderNodeMath")
        math.location = (-1000, 480)
        math.operation = 'GREATER_THAN'
        math.inputs[1].default_value = 0.1

        # add cramp1 node
        cramp1 = hsmat.node_tree.nodes.new("ShaderNodeValToRGB")
        cramp1.location = (-800, 480)

        # add gradiendtex node
        gradiendtex = hsmat.node_tree.nodes.new("ShaderNodeTexGradient")
        gradiendtex.location = (-1000, 180)
        gradiendtex.gradient_type = 'SPHERICAL'

        # add cramp2 node
        cramp2 = hsmat.node_tree.nodes.new("ShaderNodeValToRGB")
        cramp2.location = (-800, 180)
        cramp2.color_ramp.interpolation = 'CONSTANT'
        cramp2.color_ramp.elements[0].position = 0
        cramp2.color_ramp.elements[1].position = 0.5
        cramp2.color_ramp.elements[0].color = (1, 1, 1, 1)
        cramp2.color_ramp.elements[1].color = (0, 0, 0, 1)

        # add rgbmix1 node
        rgbmixer1 = hsmat.node_tree.nodes.new('ShaderNodeMix')
        rgbmixer1.data_type = 'RGBA'
        rgbmixer1.blend_type = 'MULTIPLY'
        rgbmixer1.inputs[0].default_value = 1
        rgbmixer1.location = (-500, 300)

        # add rgbmix2 node
        rgbmix2 = hsmat.node_tree.nodes.new('ShaderNodeMix')
        rgbmix2.data_type = 'RGBA'
        rgbmix2.blend_type = 'MIX'
        rgbmix2.location = (-300, 300)

        # link shaders
        hsmat.node_tree.links.new(texcord.outputs[2], sepxyz.inputs[0])
        hsmat.node_tree.links.new(texcord.outputs[2], mappcord.inputs[0])
        hsmat.node_tree.links.new(sepxyz.outputs[1], math.inputs[0])
        hsmat.node_tree.links.new(math.outputs[0], cramp1.inputs[0])
        hsmat.node_tree.links.new(mappcord.outputs[0], gradiendtex.inputs[0])
        hsmat.node_tree.links.new(gradiendtex.outputs[0], cramp2.inputs[0])
        hsmat.node_tree.links.new(cramp1.outputs[0], rgbmixer1.inputs[6])
        hsmat.node_tree.links.new(cramp2.outputs[0], rgbmixer1.inputs[7])
        hsmat.node_tree.links.new(rgbmixer1.outputs[2], rgbmix2.inputs[0])
        hsmat.node_tree.links.new(rgbmixer1.outputs[2], rgbmix2.inputs[6])
        hsmat.node_tree.links.new(rgbmix2.outputs[2], emi.inputs[0])
        hsmat.node_tree.links.new(mixer.outputs[0], hsmat_output.inputs[0])
        hsmat.node_tree.links.new(transparent.outputs[0], mixer.inputs[1])
        hsmat.node_tree.links.new(emi.outputs[0], mixer.inputs[2])
        hsmat.node_tree.links.new(color.outputs[0], rgbmix2.inputs[7])

        hsmat.use_backface_culling = True
        obj.active_material = hsmat

        return {'FINISHED'}

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)
