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
import bmesh


class PCA_OT_facesplitter(bpy.types.Operator):
    """Split Mesh"""
    bl_idname = "pca.facesplitter"
    bl_label = "Split Mesh"

    def execute(self, context):

        if bpy.context.active_object != None and bpy.context.active_object.type == 'MESH':

            obj = bpy.context.active_object
            fcs = obj.data.polygons

            if len(fcs) != 0:

                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='VERT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.select_mode(type='FACE')
                bpy.ops.mesh.select_mode(type='VERT')
                bpy.ops.mesh.select_all(action='INVERT')
                bpy.ops.mesh.delete(type='VERT')

                bm = bmesh.from_edit_mesh(obj.data)
                svts = [v for v in bm.verts if len(v.link_edges) == 0]

                for v in svts:
                    v.select = True
                    bpy.ops.mesh.delete(type='VERT')

                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles()

                bpy.ops.mesh.edge_split()

                bpy.ops.mesh.separate(type='LOOSE')

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
            else:
                self.report({'WARNING'}, 'Mesh has no polygons..')

        else:
            self.report({'WARNING'}, 'No mesh was selected')

        return {'FINISHED'}

    # popup dialog
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    # popup message
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text='', icon='ERROR')
        col.label(text="The mesh will be split into many meshes.")
        col.label(text="Each polygon will become a single mesh!")
