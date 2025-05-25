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
from . pca_funcs import cleanstr, check_if_faces
from bpy_extras.io_utils import ImportHelper

# DEPTH Material


class PCAPLUS_OT_depthmat(bpy.types.Operator, ImportHelper):
    """For finished(!) 3d depthmaps"""
    bl_idname = "pcaplus.depthmat"
    bl_label = "Depthmapped"
    bl_options = {'UNDO'}

    filter_glob: bpy.props.StringProperty(
        default='*.JPG;*.jpg;*.jpeg;*.png;*.tif;*.tiff',
        options={'HIDDEN'}
    )  # type: ignore

    inpname: bpy.props.StringProperty(
        name='Name: ',
        description='Give your material an awesome name!',
        default='My Depthmapped'
    )  # type: ignore

    fuser_boolean: bpy.props.BoolProperty(
        name='Fake User',
        description='Add a fake-user to the material',
        default=True,
    )  # type: ignore

    def execute(self, context):
        """ """
        hasFaces = False
        filename, extension = os.path.splitext(self.filepath)
        cb_protectfacemask = context.scene.cb_protectfacemask

        # check if selected file is an image
        if extension != '.jpg' and extension != '.JPG' and extension != '.jpeg' and extension != '.png' and extension != '.tif' and extension != '.tiff':
            self.report({'WARNING'}, 'Only jpg, png or tif images allowed!')
        else:

            imgpath = str(self.filepath)
            inpname = str(self.inpname)
            inpname = cleanstr(inpname)
            fu = self.fuser_boolean

            obj = bpy.context.active_object

            ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
            if cb_protectfacemask and len(obj.vertex_groups) > 0:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')

                # select vertex group, switch to edge and face mode
                bpy.ops.object.vertex_group_select()
                bpy.ops.mesh.select_mode(
                    use_extend=False, use_expand=False, type='EDGE')
                bpy.ops.mesh.select_mode(
                    use_extend=False, use_expand=False, type='FACE')

                if check_if_faces(obj) == True:
                    hasFaces = True

                    bpy.ops.mesh.separate(type='SELECTED')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.context.active_object.select_set(False)

                    # get objectcopy
                    for splitobj in bpy.context.selected_objects:
                        bpy.context.view_layer.objects.active = splitobj
                    bpy.context.active_object.select_set(False)
                    obj.select_set(True)  # Select the object
                    context.view_layer.objects.active = obj
                else:
                    self.report({'WARNING'}, "Vertexgroup contains no faces")
                    bpy.ops.object.mode_set(mode='OBJECT')

            for i in range(len(obj.material_slots)):
                obj.active_material_index = 0
                bpy.ops.object.material_slot_remove()

            stlmat = bpy.data.materials.new(name="new")
            stlmat.use_nodes = True
            stlmat.name = inpname + "_depthMAT"

            obj.active_material = stlmat

            # Remove default material
            # title of the existing node when materials.new
            stlmat.node_tree.nodes.remove(
                stlmat.node_tree.nodes.get('Principled BSDF'))
            stlmat_output = stlmat.node_tree.nodes.get('Material Output')
            # add emission shader
            emission = stlmat.node_tree.nodes.new('ShaderNodeEmission')
            emission.inputs["Color"].default_value = (0, 1, 0, 0.5)
            emission.location = (-10, 280)
            emission.inputs[0].show_expanded = True
            # STLpano texture
            stltexture = stlmat.node_tree.nodes.new('ShaderNodeTexEnvironment')
            stltexture.image = bpy.data.images.load(imgpath)
            stltexture.location = (-300, 280)
            # mapping
            stlmapping = stlmat.node_tree.nodes.new('ShaderNodeMapping')
            stlmapping.location = (-500, 280)
            stlmapping.inputs[2].default_value[2] = -1.5708

            # Texture coordinate
            stlcoordinate = stlmat.node_tree.nodes.new('ShaderNodeTexCoord')
            stlcoordinate.location = (-800, 280)

            # link shaders
            stlmat.node_tree.links.new(
                emission.outputs[0], stlmat_output.inputs[0])
            stlmat.node_tree.links.new(
                stltexture.outputs[0], emission.inputs[0])
            stlmat.node_tree.links.new(
                stlcoordinate.outputs[3], stlmapping.inputs[0])
            stlmat.node_tree.links.new(
                stlmapping.outputs[0], stltexture.inputs[0])

            # add fakeuser
            if fu == True:
                stlmat.use_fake_user = True

            # backface_culling
            bpy.context.object.active_material.use_backface_culling = True

            # join masked
            if cb_protectfacemask == True and hasFaces == True:
                splitobj.select_set(True)  # Select the object
                obj.select_set(True)  # Select the object
                context.view_layer.objects.active = obj
                bpy.ops.object.join()
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles()
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}

# UV Material


class PCAPLUS_OT_uvmat(bpy.types.Operator, ImportHelper):
    """For the dollhouse"""
    bl_idname = "pcaplus.uvmat"
    bl_label = "UV Texture"
    bl_options = {'UNDO'}

    filter_glob: bpy.props.StringProperty(
        default='*.JPG;*.jpg;*.jpeg;*.png;*.tif;*.tiff',
        options={'HIDDEN'}
    )  # type: ignore

    inpname: bpy.props.StringProperty(
        name='Name: ',
        description='Give your material an awesome name',
        default='My UV-texture'
    )  # type: ignore

    fuser_boolean: bpy.props.BoolProperty(
        name='Fake User',
        description='Add a fake-user to the material',
        default=True,
    )  # type: ignore

    def execute(self, context):

        hasFaces = False
        obj = bpy.context.active_object

        if len(obj.data.uv_layers) > 0:

            filename, extension = os.path.splitext(self.filepath)
            cb_protectfacemask = context.scene.cb_protectfacemask

            if extension != '.jpg' and extension != '.JPG' and extension != '.jpeg' and extension != '.png' and extension != '.tif' and extension != '.tiff':
                self.report(
                    {'WARNING'}, 'Only jpg, png or tif images allowed!')
            else:

                imgpath = str(self.filepath)
                inpname = str(self.inpname)
                inpname = cleanstr(inpname)
                fu = self.fuser_boolean

                obj = bpy.context.active_object

                ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
                if cb_protectfacemask and len(obj.vertex_groups) > 0:
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='DESELECT')

                    # select vertex group, switch to edge and face mode
                    bpy.ops.object.vertex_group_select()
                    bpy.ops.mesh.select_mode(
                        use_extend=False, use_expand=False, type='EDGE')
                    bpy.ops.mesh.select_mode(
                        use_extend=False, use_expand=False, type='FACE')

                    if check_if_faces(obj) == True:
                        hasFaces = True

                        bpy.ops.mesh.separate(type='SELECTED')
                        bpy.ops.object.mode_set(mode='OBJECT')
                        bpy.context.active_object.select_set(False)

                        # get objectcopy
                        for splitobj in bpy.context.selected_objects:
                            bpy.context.view_layer.objects.active = splitobj
                        bpy.context.active_object.select_set(False)
                        obj.select_set(True)  # Select the object
                        context.view_layer.objects.active = obj
                    else:
                        self.report(
                            {'WARNING'}, "Vertexgroup contains no faces")
                        bpy.ops.object.mode_set(mode='OBJECT')

                for i in range(len(obj.material_slots)):
                    obj.active_material_index = 0
                    bpy.ops.object.material_slot_remove()

                uvmat = bpy.data.materials.new(name="new")
                uvmat.use_nodes = True
                uvmat.name = inpname + "_UVMAT"

                obj.active_material = uvmat

                # Remove default material
                # title of the existing node when materials.new
                uvmat.node_tree.nodes.remove(
                    uvmat.node_tree.nodes.get('Principled BSDF'))
                uvmat_output = uvmat.node_tree.nodes.get('Material Output')
                # add emission shader
                emission = uvmat.node_tree.nodes.new('ShaderNodeEmission')
                emission.inputs["Color"].default_value = (0, 1, 0, 0.5)
                emission.location = (-10, 280)
                emission.inputs[0].show_expanded = True
                # UV texture
                uvtexture = uvmat.node_tree.nodes.new('ShaderNodeTexImage')
                uvtexture.image = bpy.data.images.load(imgpath)
                uvtexture.location = (-300, 280)
                # Texture coordinate
                uvcoordinate = uvmat.node_tree.nodes.new('ShaderNodeTexCoord')
                uvcoordinate.location = (-500, 280)

                # link shaders
                uvmat.node_tree.links.new(
                    emission.outputs[0], uvmat_output.inputs[0])
                uvmat.node_tree.links.new(
                    uvtexture.outputs[0], emission.inputs[0])
                uvmat.node_tree.links.new(
                    uvcoordinate.outputs[2], uvtexture.inputs[0])

                # fakeuser
                if fu == True:
                    uvmat.use_fake_user = True

                # backface_culling
                bpy.context.object.active_material.use_backface_culling = True

                # join masked ################
                if hasFaces == True and cb_protectfacemask == True:
                    splitobj.select_set(True)  # Select the object
                    obj.select_set(True)  # Select the object
                    context.view_layer.objects.active = obj
                    bpy.ops.object.join()
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.remove_doubles()
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.object.mode_set(mode='OBJECT')

        else:
            self.report({'ERROR'}, "Mesh has no UV-layout")

        return {'FINISHED'}

# CKECKER Material


class PCAPLUS_OT_checkmat(bpy.types.Operator):
    """For checking the UV layout"""
    bl_idname = "pcaplus.checkmat"
    bl_label = "UV Checker"
    bl_options = {'UNDO'}

    def execute(self, context):

        cb_protectfacemask = context.scene.cb_protectfacemask
        hasFaces = False

        obj = bpy.context.active_object
        objname = bpy.context.active_object.name

        obj.select_set(True)  # Select the object
        context.view_layer.objects.active = obj  # Set the object as the active object

        if len(obj.data.uv_layers) > 0:

            if cb_protectfacemask and len(obj.vertex_groups) > 0:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')

                # select vertex group, switch to edge and face mode
                bpy.ops.object.vertex_group_select()
                bpy.ops.mesh.select_mode(
                    use_extend=False, use_expand=False, type='EDGE')
                bpy.ops.mesh.select_mode(
                    use_extend=False, use_expand=False, type='FACE')

                if check_if_faces(obj) == True:
                    hasFaces = True

                    bpy.ops.mesh.separate(type='SELECTED')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.context.active_object.select_set(False)

                    # get objectcopy
                    for splitobj in bpy.context.selected_objects:
                        bpy.context.view_layer.objects.active = splitobj
                    bpy.context.active_object.select_set(False)
                    obj.select_set(True)  # Select the object
                    context.view_layer.objects.active = obj
                else:
                    self.report({'WARNING'}, "Vertexgroup contains no faces")
                    bpy.ops.object.mode_set(mode='OBJECT')

            # remove all materials
            for i in range(len(obj.material_slots)):
                obj.active_material_index = 0
                bpy.ops.object.material_slot_remove()

            matname = objname + "_CHECKERMAT"

            if matname in bpy.data.materials:
                for i in range(len(obj.material_slots)):
                    obj.active_material_index = 0
                    bpy.ops.object.material_slot_remove()

                obj.active_material = bpy.data.materials[matname]
            else:
                checkmat = bpy.data.materials.new(name="new")
                checkmat.use_nodes = True
                checkmat.name = matname

                obj.active_material = checkmat

                # Remove default material
                checkmat.node_tree.nodes.remove(checkmat.node_tree.nodes.get(
                    'Principled BSDF'))  # title of the existing node when materials.new
                checkmat_output = checkmat.node_tree.nodes.get(
                    'Material Output')
                # add emission shader
                emission = checkmat.node_tree.nodes.new('ShaderNodeEmission')
                emission.inputs["Color"].default_value = (0, 1, 0, 0.5)
                emission.location = (-10, 280)
                # UV checker texture
                checktexture = checkmat.node_tree.nodes.new(
                    'ShaderNodeTexChecker')
                checktexture.location = (-300, 280)
                checktexture.inputs[3].default_value = 10

                # Texture coordinate
                checkcoordinate = checkmat.node_tree.nodes.new(
                    'ShaderNodeTexCoord')
                checkcoordinate.location = (-500, 280)

                # link shaders
                checkmat.node_tree.links.new(
                    emission.outputs[0], checkmat_output.inputs[0])
                checkmat.node_tree.links.new(
                    checktexture.outputs[0], emission.inputs[0])
                checkmat.node_tree.links.new(
                    checkcoordinate.outputs[2], checktexture.inputs[0])
                # backface_culling
                bpy.context.object.active_material.use_backface_culling = True

            # join masked
            if cb_protectfacemask and hasFaces == True:
                splitobj.select_set(True)  # Select the object
                obj.select_set(True)  # Select the object
                context.view_layer.objects.active = obj
                bpy.ops.object.join()
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles()
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')

        else:
            self.report({'ERROR'}, "Mesh has no UV-layout")

        return {'FINISHED'}
