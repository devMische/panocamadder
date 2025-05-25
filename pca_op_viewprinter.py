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
from .pca_krpfuncs import get_krp_loc, get_krp_center, get_krp_lookat, get_krp_fov
from .pca_funcs import remove_pca_naming
import json


class PCAPLUS_OT_printview(bpy.types.Operator):
    """Print to pca.txt"""
    bl_idname = "pcaplus.printview"
    bl_label = "Print"

    def execute(self, context):
        obj = bpy.context.active_object

        cb_comment = context.scene.cb_comment
        cb_hlookat = context.scene.cb_hlookat
        cb_vlookat = context.scene.cb_vlookat
        cb_fov = context.scene.cb_fov
        cb_camtxtytz = context.scene.cb_camtxtytz
        cb_camoxoyoz = context.scene.cb_camoxoyoz
        cb_camcenter = context.scene.cb_camcenter
        cb_camorigin = context.scene.cb_camorigin

        decis = context.scene.viewdecis
        usecenter = bpy.context.preferences.addons['panocamadder'].preferences.usecenter

        cb_json = context.scene.cb_json

        if cb_json:
            jsonoutput = []

        txtname = 'pca.txt'
        if not txtname in bpy.data.texts:
            pcatxt = bpy.data.texts.new(txtname)
        else:
            pcatxt = bpy.data.texts[txtname]
            pcatxt.clear()

        objs = [obj for obj in bpy.context.selected_objects if obj.type == 'CAMERA']

        for obj in objs:

            if cb_json:
                cam = {}
                camname = remove_pca_naming(obj.name)

                cam['name'] = f'{camname}'
                cam['scene'] = f'scene_{camname}'

            # comment
            if cb_comment == True:
                pcatxt.write(f'<!-- Name={obj.name} | Type={obj.type} --> \n')

            if cb_hlookat == True:
                pcatxt.write(f'hlookat="{get_krp_lookat(obj, decis)[0]}" \n')
                if cb_json:
                    cam['hlookat'] = get_krp_lookat(obj, decis)[0]

            if cb_vlookat == True:
                pcatxt.write(f'vlookat="{get_krp_lookat(obj, decis)[1]}" \n')
                if cb_json:
                    cam['vlookat'] = get_krp_lookat(obj, decis)[1]

            if cb_fov == True:
                pcatxt.write(f'fov="{get_krp_fov(obj, decis)}" \n')
                if cb_json:
                    cam['fov'] = get_krp_fov(obj, decis)

            if cb_camtxtytz == True:
                pcatxt.write(
                    f'tx="{get_krp_loc(obj,decis)[0]}" ty="{get_krp_loc(obj,decis)[1]}" tz="{get_krp_loc(obj,decis)[2]}" \n')

            if cb_camoxoyoz == True:
                pcatxt.write(
                    f'ox="{get_krp_loc(obj,decis)[0]}" oy="{get_krp_loc(obj,decis)[1]}" oz="{get_krp_loc(obj,decis)[2]}" \n')

            # json location
            if cb_json:
                if cb_camoxoyoz == True or cb_camtxtytz == True:
                    cam['location'] = (get_krp_loc(obj, decis)[0], get_krp_loc(
                        obj, decis)[1], get_krp_loc(obj, decis)[2])

            # origin
            if cb_camorigin == True:
                pcatxt.write(
                    f'origin="{get_krp_center(obj, decis)[2]}, {get_krp_center(obj, decis)[1]}, {get_krp_center(obj, decis)[0] * -1}" \n')
                if cb_json:
                    cam['origin'] = (get_krp_center(obj, decis)[2], get_krp_center(
                        obj, decis)[1], get_krp_center(obj, decis)[0] * -1)

            # center
            if usecenter == True and cb_camcenter == True:
                pcatxt.write(
                    f'center="{get_krp_center(obj, decis)[0]}, {get_krp_center(obj, decis)[1]}, {get_krp_center(obj, decis)[2]}"  \n')
                if cb_json:
                    cam['center'] = f'{get_krp_center(obj, decis)[0]}, {get_krp_center(obj, decis)[1]}, {get_krp_center(obj, decis)[2]}'

            pcatxt.write('\n')

            if cb_json:
                jsonoutput.append(cam)

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
