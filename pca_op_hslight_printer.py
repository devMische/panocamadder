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
from .pca_krpfuncs import get_krp_loc, get_krp_sunpos, get_krp_spottarget
from . pca_funcs import floats_to_hex
from math import degrees
import json


class PCAPLUS_OT_printhslight(bpy.types.Operator):
    """Print to pca.txt"""
    bl_idname = "pcaplus.printhslight"
    bl_label = "Print Light Hotspots"

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        cb_comment = context.scene.cb_comment
        cb_hsbrackets = context.scene.cb_hsbrackets
        cb_hsstyle = context.scene.cb_hsstyle
        cb_hs_basics = context.scene.cb_hs_basics
        cb_hslight_name = context.scene.cb_hslight_name
        cb_hslight_loc = context.scene.cb_hslight_loc
        cb_hslight_col = context.scene.cb_hslight_col
        cb_hslight_target = context.scene.cb_hslight_target
        cb_hslight_energy = context.scene.cb_hslight_energy
        cb_hslight_mode = context.scene.cb_hslight_mode
        cb_hslight_spotsize = context.scene.cb_hslight_spotsize
        cb_hslight_spotblend = context.scene.cb_hslight_spotblend
        cb_hslight_shadow = context.scene.cb_hslight_shadow
        cb_hslight_distance = context.scene.cb_hslight_distance

        hs_basic_light = bpy.context.preferences.addons['panocamadder'].preferences.hs_basic_light

        cb_json = context.scene.cb_json

        if cb_json:
            jsonoutput = []

        txtname = 'pca.txt'
        if not txtname in bpy.data.texts:
            pcatxt = bpy.data.texts.new(txtname)
        else:
            pcatxt = bpy.data.texts[txtname]
            pcatxt.clear()

        modes = ['SPOT', 'SUN', 'POINT']
        decis = context.scene.hsdecis

        stylespot = context.scene.stylespot
        stylesun = context.scene.stylesun
        stylepoint = context.scene.stylepoint

        objs = [obj for obj in bpy.context.selected_objects if obj.type ==
                'LIGHT' and obj.data.type in modes]
        for obj in objs:

            obj.data.use_custom_distance = True

            obj.select_set(True)  # Select the object
            context.view_layer.objects.active = obj  # Set the object as the active object

            if obj.data.type == 'SPOT':
                obj.data.use_custom_distance = True

            if cb_json:
                hslight = {}
                hslight['name'] = f'{obj.name}'

            pcatxt.write("\n")
            if cb_comment == True:
                pcatxt.write(f'<!-- Name={obj.name} | Type={obj.type} -->\n')

            # openbracket
            if cb_hsbrackets == True:
                pcatxt.write(f'<hotspot name="{obj.name}" \n')

            # name
            if cb_hsbrackets == False and cb_hslight_name == True:
                pcatxt.write(f'name="{obj.name}" \n')

            if cb_hs_basics:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'{hs_basic_light}\n')

            # style
            if cb_hsstyle == True and obj.data.type == 'SPOT':
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'style="{stylespot}" \n')
                if cb_json:
                    hslight['style'] = f'{stylespot}'

            if cb_hsstyle == True and obj.data.type == 'SUN':
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'style="{stylesun}" \n')
                if cb_json:
                    hslight['style'] = f'{stylesun}'

            if cb_hsstyle == True and obj.data.type == 'POINT':
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'style="{stylepoint}" \n')
                if cb_json:
                    hslight['style'] = f'{stylepoint}'

            # mode
            if cb_hslight_mode == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'mode="{obj.data.type.lower()}" \n')
                if cb_json:
                    hslight['mode'] = f'{obj.data.type.lower()}'

            # location
            if cb_hslight_loc == True and obj.data.type != 'SUN':
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'tx="{get_krp_loc(obj, decis)[0]}" ty="{get_krp_loc(obj, decis)[1]}" tz="{get_krp_loc(obj, decis)[2]}" \n')
                if cb_json:
                    hslight['location'] = (get_krp_loc(obj, decis)[0], get_krp_loc(
                        obj, decis)[1], get_krp_loc(obj, decis)[2])

            # location sun
            if cb_hslight_loc == True and obj.data.type == 'SUN':
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'ath="{get_krp_sunpos(obj,decis)[0]}" atv="{get_krp_sunpos(obj,decis)[1]}" \n')
                if cb_json:
                    hslight['position'] = (get_krp_sunpos(obj, decis)[
                                           0], get_krp_sunpos(obj, decis)[1])

            # target (spot)
            if cb_hslight_target == True and obj.data.type == 'SPOT':
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'targetx="{round(get_krp_spottarget(obj)[0], decis)}" targety="{round(get_krp_spottarget(obj)[1], decis)}" targetz="{round(get_krp_spottarget(obj)[2], decis)}" \n')
                if cb_json:
                    hslight['target'] = (round(get_krp_spottarget(obj)[0], decis), round(
                        get_krp_spottarget(obj)[1], decis), round(get_krp_spottarget(obj)[2], decis))

            # spot size
            if cb_hslight_spotsize == True and obj.data.type == 'SPOT':
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'angle="{round(degrees(obj.data.spot_size), decis)}" \n')
                if cb_json:
                    hslight['angle'] = round(
                        degrees(obj.data.spot_size), decis)

            # spot blend
            if cb_hslight_spotblend == True and obj.data.type == 'SPOT':
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'penumbra="{round(obj.data.spot_blend, decis)}" \n')
                if cb_json:
                    hslight['penumbra'] = round(obj.data.spot_blend, decis)

            # distance
            if cb_hslight_distance == True:
                if obj.data.type == 'SPOT' or obj.data.type == 'POINT':
                    if obj.data.use_custom_distance == True:
                        if cb_hsbrackets:
                            pcatxt.write('    ')
                        pcatxt.write(
                            f'distance="{round(obj.data.cutoff_distance * 100, decis)}" \n')
                        if cb_json:
                            hslight['distance'] = round(
                                obj.data.cutoff_distance * 100, decis)
                    if obj.data.use_custom_distance == False:
                        if cb_hsbrackets:
                            pcatxt.write('    ')
                        pcatxt.write(f'distance="0" \n')
                        if cb_json:
                            hslight['distance'] = 0

            # intensity
            if cb_hslight_energy == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'intensity="{round(obj.data.energy / 10,decis)}" \n')
                if cb_json:
                    hslight['intensity'] = round(obj.data.energy / 10, decis)

            # color
            if cb_hslight_col == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'color="{floats_to_hex(obj.data.color[0],obj.data.color[1],obj.data.color[2])}" \n')
                if cb_json:
                    hslight['color'] = floats_to_hex(
                        obj.data.color[0], obj.data.color[1], obj.data.color[2])

            # castshadow
            if cb_hslight_shadow == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'castshadow="{str(obj.data.use_shadow).casefold()}" \n')
                if cb_json:
                    hslight['castshadow'] = obj.data.use_shadow

            # closebracket
            if cb_hsbrackets == True:
                pcatxt.write('/> \n')

            if cb_json:
                jsonoutput.append(hslight)

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
