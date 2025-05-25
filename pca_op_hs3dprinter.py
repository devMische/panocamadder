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
from .pca_krpfuncs import get_krp_loc, get_krp_rot_3d, get_krp_scale_3d
import json


class PCAPLUS_OT_prinths3d(bpy.types.Operator):
    """Print to pca.txt"""
    bl_idname = "pcaplus.prinths3d"
    bl_label = "Print 3D Hotspots"

    def execute(self, context):

        cb_json = context.scene.cb_json
        cb_comment = context.scene.cb_comment
        cb_hsbrackets = context.scene.cb_hsbrackets
        cb_hsname = context.scene.cb_hsname
        cb_hs_basics = context.scene.cb_hs_basics
        cb_hsstyle = context.scene.cb_hsstyle
        hstype = context.scene.hs_type
        stylename = context.scene.stylename
        cb_hsloc = context.scene.cb_hsloc
        cb_hsrot = context.scene.cb_hsrot
        cb_scale = context.scene.cb_scale
        cb_modelurl = context.scene.cb_modelurl
        decis = context.scene.hsdecis
        model_type = context.scene.model_type

        modelhsfolder = bpy.context.preferences.addons['panocamadder'].preferences.modelhsfolder
        hs_basic_3d = bpy.context.preferences.addons['panocamadder'].preferences.hs_basic_3d

        bpy.ops.object.mode_set(mode='OBJECT')

        if cb_json:
            jsonoutput = []

        txtname = 'pca.txt'
        if not txtname in bpy.data.texts:
            pcatxt = bpy.data.texts.new(txtname)
        else:
            pcatxt = bpy.data.texts[txtname]
            pcatxt.clear()

        objs = [obj for obj in bpy.context.selected_objects if obj.type ==
                'MESH' or obj.type == 'EMPTY']
        for obj in objs:

            obj.select_set(True)  # Select the object
            context.view_layer.objects.active = obj  # Set the object as the active object

            if cb_json:
                hs = {}
                hs['name'] = f'{obj.name}'
                hs['type'] = f'{hstype}'
                if cb_hsstyle == True:
                    hs['style'] = stylename

            pcatxt.write("\n")
            if cb_comment == True:
                pcatxt.write(f'<!-- Name={obj.name} | Type={obj.type} -->\n')

            if cb_hsbrackets == True:
                pcatxt.write(f'<hotspot name="{obj.name}" \n')

            if cb_hsname == True and cb_hsbrackets == False:
                pcatxt.write(f'name="{obj.name}" \n')

            if cb_hsstyle == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'style="{stylename}"\n')

            if cb_hs_basics == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'{hs_basic_3d} \n')

            if cb_hsloc == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'tx="{get_krp_loc(obj, decis)[0]}" ty="{get_krp_loc(obj, decis)[1]}" tz="{get_krp_loc(obj, decis)[2]}" \n')
                if cb_json:
                    hs['location'] = (get_krp_loc(obj, decis)[0], get_krp_loc(
                        obj, decis)[1], get_krp_loc(obj, decis)[2])

            if cb_hsrot == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'rx="{get_krp_rot_3d(obj, decis)[0]}" ry="{get_krp_rot_3d(obj, decis)[1]}" rz="{get_krp_rot_3d(obj, decis)[2]}" \n')
                if cb_json:
                    hs['rotation'] = (get_krp_rot_3d(obj, decis)[0], get_krp_rot_3d(
                        obj, decis)[1], get_krp_rot_3d(obj, decis)[2])

            if cb_scale == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'scalex="{get_krp_scale_3d(obj, decis)[0]}" scaley="{get_krp_scale_3d(obj, decis)[1]}" scalez="{get_krp_scale_3d(obj, decis)[2]}" \n')
                if cb_json:
                    hs['scale'] = (get_krp_scale_3d(obj, decis)[0], get_krp_scale_3d(
                        obj, decis)[1], get_krp_scale_3d(obj, decis)[2])

            # 3D model url
            if cb_modelurl == True:
                if modelhsfolder != '':
                    if cb_hsbrackets:
                        pcatxt.write('    ')
                    pcatxt.write(
                        f'url="{modelhsfolder}{obj.name}{model_type}" \n')
                    if cb_json:
                        hs['url'] = f'{modelhsfolder}{obj.name}{model_type}'
                else:
                    if cb_hsbrackets:
                        pcatxt.write('    ')
                    pcatxt.write(
                        f'url="{modelhsfolder}{obj.name}{model_type}" \n')
                    if cb_json:
                        hs['url'] = f'{modelhsfolder}{obj.name}{model_type}'

            # close brackets
            if cb_hsbrackets == True:
                pcatxt.write(f'/>\n')

            pcatxt.write('\n')
            # json
            if cb_json:
                jsonoutput.append(hs)

        # PCA JSON
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
