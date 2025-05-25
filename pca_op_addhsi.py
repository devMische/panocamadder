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
import os
from . pca_funcs import cleanstr
from bpy_extras.io_utils import ImportHelper

# Add ImageHotSpot Operator


class PCAPLUS_OT_addhsiop(bpy.types.Operator, ImportHelper):
    """Open the 'Add ImageHotspot' dialog box"""
    bl_idname = "pcaplus.hsi_filebrowser"
    bl_label = "OK"

    filter_glob: bpy.props.StringProperty(
        default='*.jpg;*.JPG;*.jpeg;*.png;*.tif;*.tiff',
        options={'HIDDEN'}
    )  # type: ignore

    pname: bpy.props.StringProperty(
        name='Name: ',
        description='The hotspot name',
        default='MyImageHotspot'
    )  # type: ignore

    def execute(self, context):

        filename, extension = os.path.splitext(self.filepath)

        # check if selected file is an image
        if extension != '.jpg' and extension != '.JPG' and extension != '.jpeg' and extension != '.png' and extension != '.tif' and extension != '.tiff':
            self.report({'WARNING'}, 'Only jpg, png or tif images allowed!')
        else:

            imgpath = str(self.filepath)
            ihsname = str(self.pname)
            ihsname = cleanstr(ihsname)

            if len(ihsname) == 0:
                ihsname = os.path.splitext(
                    os.path.basename(f'{filename}{extension}'))[0]

            # add plane
            bpy.ops.mesh.primitive_plane_add()
            bpy.context.active_object.name = ihsname

            imghs = bpy.context.active_object
            # objname = imghs.name

            # remove all materials
            for s in imghs.material_slots:
                bpy.ops.object.material_slot_remove()

            # create new mat
            ihsmat = bpy.data.materials.new(name="new")
            ihsmat.use_nodes = True
            ihsmat.name = ihsname + "_ihsMAT"
            imghs.active_material = ihsmat

            # Remove default material shader
            ihsmat.node_tree.nodes.remove(
                ihsmat.node_tree.nodes.get('Principled BSDF'))
            # get output
            ihsmatout = ihsmat.node_tree.nodes.get('Material Output')
            ihsmatout.location = (500, 280)
            # add transpmix shader
            transpmixer = ihsmat.node_tree.nodes.new('ShaderNodeMixShader')
            transpmixer.name = 'pca-hsalpha-mixer'
            transpmixer.label = 'PCA Alpha Mixer'
            transpmixer.inputs[0].default_value = 1.0
            transpmixer.location = (310, 280)
            # add emission shader
            emission = ihsmat.node_tree.nodes.new('ShaderNodeEmission')
            emission.inputs["Color"].default_value = (0, 1, 0, 0.5)
            emission.location = (-10, 280)
            emission.inputs[0].show_expanded = True
            # add transparent shader
            transp = ihsmat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
            transp.location = (-10, 100)
            transp.inputs[0].default_value = (1, 1, 1, 1.0)
            # add mix shader
            mixsh = ihsmat.node_tree.nodes.new('ShaderNodeMixShader')
            mixsh.location = (150, 180)

            # Image texture
            ihstexture = ihsmat.node_tree.nodes.new('ShaderNodeTexImage')
            ihstexture.location = (-300, 280)
            ihstexture.label = 'PCAIMGTEX'
            ihstexture.image = bpy.data.images.load(imgpath)

            # Texture coordinate
            ihscoordinate = ihsmat.node_tree.nodes.new('ShaderNodeTexCoord')
            ihscoordinate.location = (-500, 280)

            # link shaders
            ihsmat.node_tree.links.new(
                transpmixer.outputs[0], ihsmatout.inputs[0])
            ihsmat.node_tree.links.new(mixsh.outputs[0], transpmixer.inputs[2])
            ihsmat.node_tree.links.new(
                transp.outputs[0], transpmixer.inputs[1])
            ihsmat.node_tree.links.new(emission.outputs[0], mixsh.inputs[2])
            ihsmat.node_tree.links.new(transp.outputs[0], mixsh.inputs[1])
            ihsmat.node_tree.links.new(ihstexture.outputs[1], mixsh.inputs[0])

            ihsmat.node_tree.links.new(
                ihstexture.outputs[0], emission.inputs[0])
            ihsmat.node_tree.links.new(
                ihscoordinate.outputs[2], ihstexture.inputs[0])

            # alpha blend mode
            ihsmat.blend_method = 'BLEND'

            ihsmat.use_backface_culling = True

            imghs.scale[0] = ihstexture.image.size[0] / 100
            imghs.scale[1] = ihstexture.image.size[1] / 100

            imghs.show_bounds = True
            imghs.display_bounds_type = 'BOX'

            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)

        return {'FINISHED'}
