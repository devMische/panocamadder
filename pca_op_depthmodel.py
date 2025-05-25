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
from .pca_funcs import remove_pca_naming, get_pano_path


class PCAPLUS_OT_depthmodel(bpy.types.Operator):
    """Create models for using as depth models"""
    bl_label = "Create Depth Model(s)"
    bl_idname = "pcaplus.depthmodel_operator"
    bl_options = {'UNDO'}

    def execute(self, context):

        cb_tourmodel = context.scene.cb_tourmodel

        # check selection
        if len(bpy.context.selected_objects) > 1 and bpy.context.active_object.type == 'MESH':

            # create DEPTH3D collection
            depth_collection = bpy.data.collections.get('DEPTH3D')
            if depth_collection is None:
                depth_collection = bpy.data.collections.new('DEPTH3D')
                bpy.context.scene.collection.children.link(depth_collection)
                depth_collection.color_tag = 'COLOR_03'
            # create TOUR3D collection
            if cb_tourmodel == True:
                tour_collection = bpy.data.collections.get('TOUR3D')
                if tour_collection is None:
                    tour_collection = bpy.data.collections.new(
                        'TOUR3D')
                    bpy.context.scene.collection.children.link(
                        tour_collection)
                    tour_collection.color_tag = 'COLOR_07'

            model = bpy.context.active_object

            for handle in bpy.context.selected_objects:
                if handle.type == 'EMPTY' and '_HANDLE' in handle.name or handle.type == 'EMPTY' and '_EMPTY' in handle.name:

                    depthmodelname = f'{remove_pca_naming(handle.name)}_DEPTH'
                    tourmodelname = f'{remove_pca_naming(handle.name)}_TOUR'
                    depthmatname = f'{remove_pca_naming(handle.name)}_depthMAT'
                    depthmat = bpy.data.materials.get(depthmatname)

                    imgpath = get_pano_path(
                        f'{remove_pca_naming(handle.name)}_MAT')

                    # check if depthmodel already exists and delete it
                    if bpy.data.objects.get(depthmodelname) is not None:
                        bpy.ops.object.select_all(action='DESELECT')
                        bpy.data.objects[depthmodelname].select_set(True)
                        bpy.ops.object.delete(use_global=False)
                    # check if tourmodel already exists and delete it
                    if bpy.data.objects.get(tourmodelname) is not None and cb_tourmodel == True:
                        bpy.ops.object.select_all(action='DESELECT')
                        bpy.data.objects[tourmodelname].select_set(True)
                        bpy.ops.object.delete(use_global=False)

                    bpy.context.object.rotation_mode = 'XYZ'
                    rx = handle.rotation_euler[0]
                    ry = handle.rotation_euler[1]
                    rz = handle.rotation_euler[2]

                    xrev = (-1 * rx)
                    yrev = (-1 * ry)
                    zrev = (-1 * rz)

                    # cursor to empty
                    bpy.context.scene.cursor.location = handle.location

                    # create model_copy add to TOUR3D collection
                    model_copy = model.copy()
                    model_copy.data = model.data.copy()
                    if cb_tourmodel == True:
                        bpy.data.collections['TOUR3D'].objects.link(
                            model_copy)
                    else:
                        bpy.data.collections['DEPTH3D'].objects.link(
                            model_copy)

                    # select model_copy
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = model_copy
                    bpy.context.active_object.select_set(state=True)

                    # set origin / preapply rotation
                    bpy.ops.object.origin_set(
                        type='ORIGIN_CURSOR', center='MEDIAN')
                    bpy.ops.object.transform_apply(
                        location=False, rotation=True, scale=False)

                    model_copy.rotation_euler[0] = xrev
                    model_copy.rotation_euler[1] = yrev
                    model_copy.rotation_euler[2] = zrev

                    model_copy.rotation_mode = 'ZYX'
                    bpy.ops.object.transform_apply(
                        location=False, rotation=True, scale=True)
                    model_copy.rotation_mode = 'XYZ'

                    model_copy.rotation_euler[0] = rx
                    model_copy.rotation_euler[1] = ry
                    model_copy.rotation_euler[2] = rz

                    # remove all materials from model_copy
                    for i in range(len(model_copy.material_slots)):
                        model_copy.active_material_index = 0
                        bpy.ops.object.material_slot_remove()

                    if depthmat is not None:
                        model_copy.active_material = depthmat
                    else:
                        # create new material
                        if imgpath is not None:
                            depthmat = bpy.data.materials.new(
                                name=depthmatname)
                            depthmat.use_nodes = True
                            depthmat.node_tree.nodes.clear()

                            depthmat_output = depthmat.node_tree.nodes.new(
                                type='ShaderNodeOutputMaterial')
                            depthmat_output.location = (0, 0)

                            emission = depthmat.node_tree.nodes.new(
                                'ShaderNodeEmission')
                            emission.inputs["Color"].default_value = (
                                0, 1, 0, 0.5)
                            emission.location = (-10, 280)
                            emission.inputs[0].show_expanded = True
                            # depthpano texture
                            depthtexture = depthmat.node_tree.nodes.new(
                                'ShaderNodeTexEnvironment')
                            depthtexture.image = bpy.data.images.load(imgpath)
                            depthtexture.location = (-300, 280)
                            # mapping
                            mapping = depthmat.node_tree.nodes.new(
                                'ShaderNodeMapping')
                            mapping.location = (-500, 280)
                            mapping.inputs[2].default_value[2] = -1.5708

                            # Texture coordinate
                            coordinate = depthmat.node_tree.nodes.new(
                                'ShaderNodeTexCoord')
                            coordinate.location = (-800, 280)

                            # link shaders
                            depthmat.node_tree.links.new(
                                emission.outputs[0], depthmat_output.inputs[0])
                            depthmat.node_tree.links.new(
                                depthtexture.outputs[0], emission.inputs[0])
                            depthmat.node_tree.links.new(
                                coordinate.outputs[3], mapping.inputs[0])
                            depthmat.node_tree.links.new(
                                mapping.outputs[0], depthtexture.inputs[0])

                            depthmat.use_backface_culling = True
                            model_copy.active_material = depthmat

                    if cb_tourmodel == False:  # use depth model only

                        model_copy.name = depthmodelname

                        bpy.ops.object.select_all(action='DESELECT')
                        bpy.context.view_layer.objects.active = model_copy
                        bpy.context.active_object.select_set(state=True)
                        # clear rot/loc/sca
                        bpy.ops.object.rotation_clear(clear_delta=False)
                        bpy.ops.object.location_clear(clear_delta=False)
                        bpy.ops.object.scale_clear(clear_delta=False)

                        bpy.ops.object.select_all(action='DESELECT')

                    else:  # use depth and tour model

                        model_copy.name = tourmodelname

                        # create modeldepth add to collection
                        model_depth = model_copy.copy()
                        model_depth.data = model_depth.data.copy()
                        model_depth.name = depthmodelname

                        bpy.data.collections['DEPTH3D'].objects.link(
                            model_depth)

                        # select model_depth
                        bpy.ops.object.select_all(action='DESELECT')
                        bpy.context.view_layer.objects.active = model_depth
                        bpy.context.active_object.select_set(state=True)
                        # clear rot/loc/sca
                        bpy.ops.object.rotation_clear(clear_delta=False)
                        bpy.ops.object.location_clear(clear_delta=False)
                        bpy.ops.object.scale_clear(clear_delta=False)

                        bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}
