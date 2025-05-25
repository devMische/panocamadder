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
import json


class PCA_OT_printpolypoints(bpy.types.Operator):
    """Print Points3D to pca.txt"""
    bl_idname = "pca.printpolypoints"
    bl_label = "print points"

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')

        cb_poly_comment = context.scene.cb_poly_comment
        wm = bpy.context.window_manager
        polyname = bpy.context.scene.pgname
        polyname = cleanstr(polyname)
        polystyle = bpy.context.scene.pgstyle
        polystyle = cleanstr(polystyle)
        t = 0

        cb_json = context.scene.cb_json

        if cb_json:
            jsonoutput = []

        txtname = 'pca.txt'
        if not txtname in bpy.data.texts:
            pcatxt = bpy.data.texts.new(txtname)
        else:
            pcatxt = bpy.data.texts[txtname]
            pcatxt.clear()

        objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        for o in objs:

            if cb_json:
                ps = {}
                strpoints = ''

            f = False

            if len(o.data.polygons) != 0:
                f = True

            t += 1

            o.select_set(True)  # Select the object
            context.view_layer.objects.active = o  # Set the object as the active object

            # progress
            tot = 100
            wm.progress_begin(0, tot)
            for i in range(tot):
                wm.progress_update(i)
            wm.progress_end()

            bpy.ops.object.convert(target='CURVE')

            if o.type != 'CURVE':
                self.report(
                    {'WARNING'}, f'Something went wrong.. object: "{o.name}" is not planar..')
            else:
                bpy.ops.object.convert(target='MESH')

                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action='SELECT')

                if f == True:
                    bpy.ops.mesh.edge_face_add()

                bpy.ops.object.editmode_toggle()

                obj = bpy.context.active_object
                vts = obj.data.vertices

                x = 0

                if cb_poly_comment == True:
                    pcatxt.write(f'<!-- Object: {obj.name} --> \n')

                if len(objs) > 1:
                    pcatxt.write(
                        f'<hotspot name="{polyname}{t}" style="{polystyle}" points3d="')
                    if cb_json:
                        ps['name'] = f'{polyname}{t}'
                        ps['meshname'] = f'{obj.name}'
                        ps['style'] = f'{polystyle}'
                else:
                    pcatxt.write(
                        f'<hotspot name="{polyname}" style="{polystyle}" points3d="')
                    if cb_json:
                        ps['name'] = f'{polyname}'
                        ps['meshname'] = f'{obj.name}'
                        ps['style'] = f'{polystyle}'

                for v in vts:

                    v_local = vts[x].co  # local vertex coordinate
                    v_global = obj.matrix_world @ v_local  # global vertex coordinates

                    krx = round(v_global[0] * 100, 2)
                    kry = round(v_global[2] * -100, 2)
                    krz = round(v_global[1] * 100, 2)

                    if (x < len(vts) - 1):
                        pcatxt.write(f'{krx}, {kry}, {krz}, ')
                        if cb_json:
                            strpoints += f'{krx}, {kry}, {krz}, '
                    else:
                        pcatxt.write(f'{krx}, {kry}, {krz}" ')
                        if cb_json:
                            strpoints += f'{krx}, {kry}, {krz}'

                    x += 1

                pcatxt.write('/>\n')

            if cb_json:
                ps['points3d'] = f'{strpoints}'
                jsonoutput.append(ps)

        if cb_json:

            pcajson = json.dumps(jsonoutput, indent=4)

            jsonname = 'pca.JSON'
            if not jsonname in bpy.data.texts:
                jsonfile = bpy.data.texts.new(jsonname)
            else:
                jsonfile = bpy.data.texts[jsonname]

            jsonfile.clear()
            jsonfile.write(pcajson)

        return {'FINISHED'}

    # popup dialog
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    # popup message
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text='', icon='ERROR')
        col.label(text="Print the points for each selected mesh.")
        col.label(text="This can damage the UV-layout!")
        col.label(text="The process may take some time...")
