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
import json
from .pca_krpfuncs import get_krp_loc, get_krp_center, get_krp_align, get_krp_prealign
from . pca_funcs import remove_pca_naming


class PCAPLUS_OT_printpano(bpy.types.Operator):
    """Print to pca.txt"""
    bl_idname = "pcaplus.printpano"
    bl_label = "Print"

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')

        decis = context.scene.panodecis
        pano_extension = bpy.context.preferences.addons['panocamadder'].preferences.pano_extension

        cb_comment = context.scene.cb_comment
        cb_panostyle = context.scene.cb_panostyle
        cb_txtytz = context.scene.cb_txtytz
        cb_oxoyoz = context.scene.cb_oxoyoz
        cb_center = context.scene.cb_center
        cb_origin = context.scene.cb_origin
        cb_align = context.scene.cb_align
        cb_prealign = context.scene.cb_prealign

        cb_json = context.scene.cb_json
        cb_pcijson = context.scene.cb_pcijson
        usecenter = bpy.context.preferences.addons['panocamadder'].preferences.usecenter
        uselinkedscene = bpy.context.preferences.addons['panocamadder'].preferences.uselinkedscene

        if cb_json:
            jsonoutput = []
        if cb_pcijson:
            pcioutput = []

        # PCA text file
        txtname = 'pca.txt'
        if not txtname in bpy.data.texts:
            pcatxt = bpy.data.texts.new(txtname)
        else:
            pcatxt = bpy.data.texts[txtname]
            pcatxt.clear()

        objs = [obj for obj in bpy.context.selected_objects if obj.type ==
                'MESH' or obj.type == 'EMPTY']
        for obj in objs:

            panoname = remove_pca_naming(obj.name)

            if cb_json:
                pano = {}
                pano['name'] = f'{panoname}'
                pano['pano'] = f'{panoname}.{pano_extension}'
                pano['scene'] = f'scene_{panoname.lower()}'
            if cb_pcijson:
                pci = {}
                pci['pano'] = f'{panoname}.{pano_extension}'
                pci['location'] = (round(obj.location[0], decis), round(
                    obj.location[1], decis), round(obj.location[2], decis))
                pci['rotation'] = (round(obj.rotation_euler[0], decis), round(
                    obj.rotation_euler[1], decis), round(obj.rotation_euler[2], decis))

            pcatxt.write("\n")
            # comment
            if cb_comment == True:
                pcatxt.write(f'<!-- Name={obj.name} | Type={obj.type} -->\n')

            # style
            if cb_panostyle == True:
                stylename = panoname + '_STYLE'
                pcatxt.write(f'<style name="{stylename}"\n')
                if cb_json:
                    pano['style'] = f'{stylename}'

            # txtytz
            if cb_txtytz == True:
                if cb_panostyle:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'tx="{get_krp_loc(obj,decis)[0]}" ty="{get_krp_loc(obj,decis)[1]}" tz="{get_krp_loc(obj,decis)[2]}"\n')

            # oxoyoz
            if cb_oxoyoz == True:
                if cb_panostyle:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'ox="{get_krp_loc(obj,decis)[0]}" oy="{get_krp_loc(obj,decis)[1]}" oz="{get_krp_loc(obj,decis)[2]}"\n')

            # JSON location (oxoyoz/txtytz)
            if cb_json:
                if cb_oxoyoz == True or cb_txtytz == True:
                    pano['location'] = (get_krp_loc(obj, decis)[0], get_krp_loc(
                        obj, decis)[1], get_krp_loc(obj, decis)[2])

            # origin
            if cb_origin == True:
                if cb_panostyle:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'origin="{get_krp_center(obj, decis)[2]}, {get_krp_center(obj, decis)[1]}, {get_krp_center(obj, decis)[0] * -1}"\n')

                if cb_json:
                    pano['origin'] = (get_krp_center(obj, decis)[2], get_krp_center(
                        obj, decis)[1], get_krp_center(obj, decis)[0] * -1)

            # center
            if cb_center == True and usecenter == True:
                if cb_panostyle:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'center="{get_krp_center(obj, decis)[0]}, {get_krp_center(obj, decis)[1]}, {get_krp_center(obj, decis)[2]}"\n')
                if cb_json:
                    pano['center'] = (get_krp_center(obj, decis)[0], get_krp_center(
                        obj, decis)[1], get_krp_center(obj, decis)[2])

            # align
            if cb_align == True:
                if cb_panostyle:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'align="{get_krp_align(obj, decis)[0]}|{get_krp_align(obj, decis)[1]}|{get_krp_align(obj, decis)[2]}"\n')
                if cb_json:
                    pano['align'] = (get_krp_align(obj, decis)[0], get_krp_align(
                        obj, decis)[1], get_krp_align(obj, decis)[2])

            # prealign
            if cb_prealign == True:
                if cb_panostyle:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'prealign="{get_krp_prealign(obj, decis)[0]}|{get_krp_prealign(obj, decis)[1]}|{get_krp_prealign(obj, decis)[2]}"\n')
                if cb_json:
                    pano['prealign'] = (get_krp_prealign(obj, decis)[0], get_krp_prealign(
                        obj, decis)[1], get_krp_prealign(obj, decis)[2])

            # style
            if cb_panostyle == True:
                if uselinkedscene == True:
                    pcatxt.write(
                        f'    linkedscene="scene_{panoname.lower()}"\n/>\n')
                else:
                    pcatxt.write('\n/>\n')

            if cb_json:
                jsonoutput.append(pano)

            if cb_pcijson:
                pcioutput.append(pci)

        # PCA JSON
        if cb_json:
            pcajson = json.dumps(jsonoutput, indent=4)

            txtname = 'pca.JSON'
            if not txtname in bpy.data.texts:
                pcatxt = bpy.data.texts.new(txtname)
            else:
                pcatxt = bpy.data.texts[txtname]

            pcatxt.clear()
            pcatxt.write(pcajson)

        # PCI JSON
        if cb_pcijson:
            pcijson = json.dumps(pcioutput, indent=4)

            pcijsonname = 'pci.JSON'
            if not pcijsonname in bpy.data.texts:
                pcijsonfile = bpy.data.texts.new(pcijsonname)
            else:
                pcijsonfile = bpy.data.texts[pcijsonname]

            pcijsonfile.clear()
            pcijsonfile.write(pcijson)

        return {'FINISHED'}
