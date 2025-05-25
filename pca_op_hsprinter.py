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
from .pca_krpfuncs import get_krp_loc, get_krp_rot, get_krp_wh, get_krp_scale
from . pca_funcs import get_pca_img_texture, get_pca_color, get_pca_alpha, check_if_hs_color, check_if_hs_alpha
import json


class PCAPLUS_OT_prinths(bpy.types.Operator):
    """Print to pca.txt"""
    bl_idname = "pcaplus.prinths"
    bl_label = "Print 2D Hotspots"

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')

        imagehsfolder = bpy.context.preferences.addons['panocamadder'].preferences.imagehsfolder

        cb_comment = context.scene.cb_comment
        cb_hsbrackets = context.scene.cb_hsbrackets
        cb_hsname = context.scene.cb_hsname
        cb_hstype = context.scene.cb_hstype
        cb_hsstyle = context.scene.cb_hsstyle
        cb_scale = context.scene.cb_scale
        cb_hs_basics = context.scene.cb_hs_basics
        cb_hsloc = context.scene.cb_hsloc
        cb_hsrot = context.scene.cb_hsrot
        cb_wh = context.scene.cb_wh
        cb_roundedge = context.scene.cb_roundedge
        cb_bgcolor = context.scene.cb_bgcolor
        cb_alpha = context.scene.cb_alpha
        cb_imgurl = context.scene.cb_imgurl

        hs_basic_2d = bpy.context.preferences.addons['panocamadder'].preferences.hs_basic_2d
        cb_json = context.scene.cb_json

        hstype = context.scene.hs_type

        decis = context.scene.hsdecis
        stylename = context.scene.stylename
        roundedge = context.scene.roundedge

        if cb_json:
            jsonoutput = []

        txtname = 'pca.txt'
        if not txtname in bpy.data.texts:
            pcatxt = bpy.data.texts.new(txtname)
        else:
            pcatxt = bpy.data.texts[txtname]
            pcatxt.clear()

        objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        for obj in objs:

            obj.select_set(True)  # Select the object
            context.view_layer.objects.active = obj  # Set the object as the active object

            # Set the origin to the geometry center for 2D hotspots
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

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

            if cb_hstype == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'type="{hstype}"\n')

            if cb_hs_basics == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'{hs_basic_2d} \n')

            if cb_hsloc == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'tx="{get_krp_loc(obj, decis)[0]}" ty="{get_krp_loc(obj, decis)[1]}" tz="{get_krp_loc(obj, decis)[2]}"\n')
                if cb_json:
                    hs['location'] = (get_krp_loc(obj, decis)[0], get_krp_loc(
                        obj, decis)[1], get_krp_loc(obj, decis)[2])

            if cb_hsrot == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'rx="{get_krp_rot(obj, decis)[0]}" ry="{get_krp_rot(obj, decis)[1]}" rz="{get_krp_rot(obj, decis)[2]}" \n')
                if cb_json:
                    hs['rotation'] = (get_krp_rot(obj, decis)[0], get_krp_rot(
                        obj, decis)[1], get_krp_rot(obj, decis)[2])

            if cb_wh == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(
                    f'width="{get_krp_wh(obj)[0]}" height="{get_krp_wh(obj)[1]}"\n')
                if cb_json:
                    hs['width'] = get_krp_wh(obj)[0]
                    hs['height'] = get_krp_wh(obj)[1]

            if hstype == 'text' and cb_roundedge == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'bgroundedge="{roundedge}" \n')
                if cb_json:
                    hs['roundedge'] = roundedge

            if cb_scale == True:
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'scale="{get_krp_scale(obj, decis)}" \n')
                if cb_json:
                    hs['scale'] = get_krp_scale(obj, decis)

            if cb_bgcolor == True and hstype == 'text' and check_if_hs_color(obj):
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'bgcolor="{get_pca_color(obj)}" \n')
                if cb_json:
                    hs['bgcolor'] = f'{get_pca_color(obj)}'

            if cb_imgurl == True and hstype == 'image':
                if imagehsfolder != '':
                    if cb_hsbrackets:
                        pcatxt.write('    ')
                    pcatxt.write(
                        f'url="{imagehsfolder}{get_pca_img_texture(obj)}" \n')
                    if cb_json:
                        hs['url'] = f'{imagehsfolder}{get_pca_img_texture(obj)}'
                else:
                    if cb_hsbrackets:
                        pcatxt.write('    ')
                    pcatxt.write(f'url="{get_pca_img_texture(obj)}" \n')
                    if cb_json:
                        hs['url'] = f'{get_pca_img_texture(obj)}'

            if cb_alpha == True and check_if_hs_alpha(obj):
                if cb_hsbrackets:
                    pcatxt.write('    ')
                pcatxt.write(f'alpha="{get_pca_alpha(obj, decis)}" \n')
                if cb_json:
                    hs['alpha'] = get_pca_alpha(obj, decis)

            if cb_hsbrackets == True:
                pcatxt.write(f'/>\n')

            pcatxt.write('\n')

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

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    # popup message

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text='', icon='ERROR')
        col.label(text="The origin will be set to the center.")
        col.label(text="Keep sure the selected object is a hotspot!")


class PCAPLUS_OT_centerorigin(bpy.types.Operator):
    """Set origin to the center"""
    bl_idname = "pcaplus.centerorigin"
    bl_label = "center origin"

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object found.")
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        return {'FINISHED'}
