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
from . pca_funcs import replace_last, check_if_faces


class PCAPLUS_OT_look360cam(bpy.types.Operator):
    """ Activate selected camera"""
    bl_idname = "pcaplus.cam360"
    bl_label = "Set 360° View"

    def execute(self, context):

        if context.scene.camera is None:
            self.report({'WARNING'}, "No camera found ..")
            return {'CANCELLED'}
        else:

            hasFaces = False

            bpy.context.space_data.camera = bpy.context.scene.camera
            bpy.context.space_data.use_local_camera = True
            bpy.context.space_data.lock_camera = True

            cb_matworld = context.scene.cb_matworld
            cb_protectfacemask = context.scene.cb_protectfacemask

            if cb_matworld == True:
                if context.mode == 'OBJECT':
                    er = False
                    ertext = ''

                    # world
                    wo = bpy.context.scene.camera.name
                    worldname = replace_last(wo, "_CAM", "_WORLD")
                    if worldname in bpy.data.worlds:
                        bpy.context.scene.world = bpy.data.worlds[worldname]
                    else:
                        er = True
                        ertext += 'no world found .. '

                    # material
                    obj = bpy.context.active_object
                    if obj.type == 'MESH':

                        obj.select_set(True)  # Select the object
                        context.view_layer.objects.active = obj  # Set the object as the active object

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

                        ma = bpy.context.scene.camera.name
                        matname = replace_last(ma, "_CAM", "_MAT")

                        if matname in bpy.data.materials:
                            for i in range(len(obj.material_slots)):
                                obj.active_material_index = 0
                                bpy.ops.object.material_slot_remove()

                            obj.active_material = bpy.data.materials[matname]
                        else:
                            er = True
                            ertext += 'no material found .. '

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
                        er = True
                        ertext += 'no MESH selected .. '

                    if er == True:
                        self.report({'WARNING'}, ertext)
                else:
                    self.report(
                        {'WARNING'}, "Can't apply material. Switch to object-mode!")

            return {'FINISHED'}


class PCAPLUS_OT_topcam(bpy.types.Operator):
    """Zenith View"""
    bl_idname = "pcaplus.topview"
    bl_label = "Zenith View"

    def execute(self, context):

        cam = context.object

        cam.rotation_euler[0] = 3.14159
        cam.rotation_euler[1] = 0

        return {'FINISHED'}


class PCAPLUS_OT_horizoncam(bpy.types.Operator):
    """Horizontal View"""
    bl_idname = "pcaplus.horizonview"
    bl_label = "Horizontal View"

    def execute(self, context):

        cam = context.object

        cam.rotation_euler[0] = 1.5708
        cam.rotation_euler[1] = 0

        return {'FINISHED'}


class PCAPLUS_OT_downcam(bpy.types.Operator):
    """Nadir View"""
    bl_idname = "pcaplus.downview"
    bl_label = "Nadir View"

    def execute(self, context):

        cam = context.object

        cam.rotation_euler[0] = 0
        cam.rotation_euler[1] = 0

        return {'FINISHED'}
