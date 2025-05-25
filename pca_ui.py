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
from .pca_krpfuncs import *
from . pca_funcs import remove_pca_naming, get_pca_img_texture, floats_to_hex
from math import degrees


class PCAPLUS_PT_main(bpy.types.Panel):
    bl_label = "PanoCamAdder 2.3"
    bl_idname = "PCAPLUS_PT_Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"

    def draw(self, context):
        if context.mode == 'OBJECT':

            layout = self.layout
            col = layout.column(align=True)
            col.operator("pcaplus.addpcop",
                         icon='CON_CAMERASOLVER', text="Add PanoCam")
            col.operator("pcaplus.addhsop", icon='MOD_MASK')
            col.operator("pcaplus.hsi_filebrowser",
                         icon='FILE_IMAGE', text="Add ImageHotspot")
            layout.scale_y = 1.3

        else:

            layout = self.layout
            box = layout.box()
            box.label(text=" Switch to object-mode")


class PCAPLUS_PT_pcimporter(bpy.types.Panel):

    bl_label = "PanoCam Import"
    bl_idname = "PCAPLUSPCI_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUS_PT_Main'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        jsonfile = context.scene.jsonfile
        pcijson = context.scene.pcijson

        if context.mode == 'OBJECT':

            layout = self.layout
            col = layout.column()
            col.operator("pca.loadpcijson", icon='CONSOLE')
            if (len(pcijson) > 0):
                layout = self.layout
                row = layout.row()

                row.label(text=f"{jsonfile} ({len(pcijson)} panoramas)")
            else:

                row = layout.row()
                row.label(text=f"{jsonfile} ..no PCI data")

            # LOCATION
            box = layout.box()
            col = box.column()
            col.label(text='Location')
            row = box.row()
            row.label(text='X:')
            row.prop(context.scene, "json_loc_x", text='')
            row.prop(context.scene, "loc_x_operator", text='')
            if context.scene.loc_x_operator != 'no':
                row.prop(context.scene, "loc_x_nmbr", text='')
            else:
                row.label(text='')

            row = box.row()
            row.label(text='Y:')
            row.prop(context.scene, "json_loc_y", text='')
            row.prop(context.scene, "loc_y_operator", text='')
            if context.scene.loc_y_operator != 'no':
                row.prop(context.scene, "loc_y_nmbr", text='')
            else:
                row.label(text='')

            row = box.row()
            row.label(text='Z:')
            row.prop(context.scene, "json_loc_z", text='')
            row.prop(context.scene, "loc_z_operator", text='')
            if context.scene.loc_z_operator != 'no':
                row.prop(context.scene, "loc_z_nmbr", text='')
            else:
                row.label(text='')

            # ROTATION
            box = layout.box()
            row = box.row()
            row.label(text='Rotation')
            row.prop(context.scene, "rad_or_deg", text='')
            row.label(text='')
            row.label(text='')

            row = box.row()
            row.label(text='X:')
            row.prop(context.scene, "json_rot_x", text='')
            row.prop(context.scene, "rot_x_operator", text='')
            if context.scene.rot_x_operator != 'no':
                row.prop(context.scene, "rot_x_nmbr", text='')
            else:
                row.label(text='')

            row = box.row()
            row.label(text='Y:')
            row.prop(context.scene, "json_rot_y", text='')
            row.prop(context.scene, "rot_y_operator", text='')
            if context.scene.rot_y_operator != 'no':
                row.prop(context.scene, "rot_y_nmbr", text='')
            else:
                row.label(text='')

            row = box.row()
            row.label(text='Z:')
            row.prop(context.scene, "json_rot_z", text='')
            row.prop(context.scene, "rot_z_operator", text='')
            if context.scene.rot_z_operator != 'no':
                row.prop(context.scene, "rot_z_nmbr", text='')
            else:
                row.label(text='')

            if (len(pcijson) > 0):
                panonmbr = context.scene.panonmbr

                layout = self.layout
                row = layout.row()
                row.label(text=f"{pcijson[panonmbr - 1]['pano']}")
                row.prop(context.scene, "panonmbr", text='')
                row.operator("pca.createsinglepci", icon='CON_CAMERASOLVER')
                col = layout.column()
                col.operator("pca.createallpci", icon='CON_CAMERASOLVER')

        else:

            layout = self.layout
            box = layout.box()
            box.label(text=" Switch to object-mode")


class PCAPLUS_PT_krptoblender(bpy.types.Panel):

    bl_label = "move to / rotate to"
    bl_idname = "PCAPLUSKTOB_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUSPCI_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout
        box = layout.box()
        box.label(text="Insert KRP code:", icon="CONSOLE")
        box.prop(context.scene, "krpcode", text='')
        if context.mode == 'OBJECT':
            col = box.column(align=True)
            col.operator("pcaplus.todcenter", text='move to center / origin')
            col.operator("pcaplus.tooxoyoz", text='move to ox/oy/oz  tx/ty/tz')
            col.operator("pcaplus.toprealign", text='rotate to (pre)align')
            col.operator("pcaplus.torxryrz", text='rotate to rx/ry/rz')
        else:
            box.label(text=" Switch to object-mode")

      # Camera Panel


class PCAPLUS_PT_camera(bpy.types.Panel):
    """Camera Settings"""
    bl_label = "PanoCam Viewer"
    bl_idname = "PCAPLUSCAMERA_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUS_PT_Main'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        obj = bpy.context.active_object

        scene = context.scene

        layout = self.layout

        col = layout.column()
        col.prop(scene, "camera", text="")
        col.operator("pcaplus.cam360", icon='CHECKBOX_HLT', text="OK")

        if len(bpy.context.selected_objects) > 0 and obj.type == 'MESH':
            row = col.row()
            row.prop(scene, "cb_matworld", text='Assign PanoMAT')
            row.prop(scene, "cb_protectfacemask", text='Protect Vertex Group')

        if len(bpy.context.selected_objects) > 0 and obj.type == 'CAMERA':

            cam = bpy.context.object.data

            layout = self.layout
            layout.separator(factor=1)
            col = layout.column()
            col.prop(cam, "lens")

            row = layout.row(align=True)
            row.operator("pcaplus.topview", icon='SORT_DESC', text="Zenith")
            row.operator("pcaplus.horizonview",
                         icon='ARROW_LEFTRIGHT', text="Horizon")
            row.operator("pcaplus.downview", icon='SORT_ASC', text="Nadir")

            row = layout.row()
            row.prop(cam, "show_composition_thirds", text="Composition Lines")
            row.prop(cam, "show_composition_center", text="Center")

      # ViewPort Panel


class PCAPLUS_PT_helpers(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Helpers / Materials / Viewport"
    bl_idname = "PCAPLUS_PT_Helpers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUS_PT_Main'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout
        col = layout.column(align=True)
        col.operator("mesh.flip_normals")
        col.operator("mesh.merge", text="Merge Verticies")
        col.operator("mesh.remove_doubles", text="Remove Doubles")

      # HelperMaterials Panel


class PCAPLUS_PT_helpermaterials(bpy.types.Panel):

    bl_label = "Materials"
    bl_idname = "PCAPLUS_PT_Helpermaterials_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUS_PT_Helpers'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        if context.mode == 'OBJECT':
            scene = context.scene
            obj = bpy.context.active_object
            if len(bpy.context.selected_objects) > 0 and obj.type == 'MESH':

                layout = self.layout
                col = layout.column()
                col.prop(scene, "cb_protectfacemask",
                         text='Protect Vertex Group')

                col = layout.column(align=True)
                col.operator("pcaplus.depthmat", icon='MESH_UVSPHERE')
                col.operator("pcaplus.uvmat", icon='IMAGE_RGB_ALPHA')
                col.operator("pcaplus.checkmat", icon='TEXTURE')

                obj = bpy.context.object
                if obj is not None and obj.type == 'MESH':

                    # if checker
                    obj = bpy.context.active_object
                    for s in obj.material_slots:
                        if s.material and s.material.use_nodes:
                            for n in s.material.node_tree.nodes:
                                if n.type == 'TEX_CHECKER':

                                    checkerscale = n.inputs[3]
                                    layout = self.layout
                                    col = layout.column()
                                    col.prop(
                                        checkerscale, "default_value", text="Checkerscale:")
            else:
                layout = self.layout
                box = layout.box()
                box.label(text=" Select a mesh")
        else:

            layout = self.layout
            box = layout.box()
            box.label(text=" Switch to object-mode")

      # Export Panel


class PCAPLUS_PT_viewport(bpy.types.Panel):
    """Toggle Viewport Settings"""
    bl_label = "Viewport Settings"
    bl_idname = "PCAPLUSVIEWPORT_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUS_PT_Helpers'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        space_data = bpy.context.space_data
        overlay = space_data.overlay
        shading = space_data.shading

        layout = self.layout
        row = layout.row()
        row.prop(overlay, "show_wireframes", text="Wireframe")
        if overlay.show_wireframes == True:
            row.prop(overlay, "wireframe_threshold", text="Threshold")
        row = layout.row()
        row.prop(overlay, "show_face_orientation", text="FaceOrientation")
        row.prop(shading, "use_scene_world", text="Background")
        layout.separator(factor=1.5)
        row = layout.row()
        row.prop(overlay, "show_stats", text="Statistics")
        row.prop(overlay, "show_text", text="Text Info")
        row.prop(overlay, "show_floor", text="Floor")
        row = layout.row()
        row.prop(overlay, "show_extras", text="Extras")
        row.prop(overlay, "show_relationship_lines", text="Relationship Lines")
        row.prop(overlay, "show_light_colors", text="Light Colors")
        row = layout.row()
        row.prop(space_data, "show_gizmo_navigate", text="Gizmo Navigation")


class PCAPLUS_PT_export(bpy.types.Panel):
    """Toggle Viewport Settings"""
    bl_label = "Depth Model"
    bl_idname = "PCAPLUSEXPORT_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUS_PT_Main'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        if context.mode == 'OBJECT':
            layout = self.layout
            row = layout.column()
            row.operator("pcaplus.depthmodel_operator", icon='CUBE')
            row.prop(context.scene, "cb_tourmodel",
                     text='Create additional TOUR arrangement')
        else:
            layout = self.layout
            box = layout.box()
            box.label(text=" Switch to object-mode")


class PCAPLUS_PT_exportinfo(bpy.types.Panel):

    bl_label = "info"
    bl_idname = "PCAPLUSEXPORTINFO_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUSEXPORT_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout
        col = layout.column(align=True)
        col.label(text="1: Select one ore more '_HANDLE'  and the model")
        col.label(text="2: Keep sure model is active object !")
        col.label(text="3: Click 'Create Depth Model'")

    # KRpanoValues Panel


class PCAPLUS_PT_krpano(bpy.types.Panel):
    """krpano values"""
    bl_label = "KRPANO Values"
    bl_idname = "PCAPLUSKRPANO_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUS_PT_Main'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        obj = bpy.context.active_object
        if obj != None:
            layout = self.layout
            box = layout.box()
            box.label(text=f'Object: {obj.name} ({obj.type})')

      # DepthPanoValue Panel


class PCAPLUS_PT_krpanodepthpano(bpy.types.Panel):

    bl_label = "Depthmap/Panorama"
    bl_idname = "PCAPLUSKRPANODEPTHPANO_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUSKRPANO_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        obj = bpy.context.active_object

        if obj != None:
            if obj.type == 'MESH' or obj.type == 'EMPTY':

                stylename = f'{remove_pca_naming(obj.name)}_STYLE'

                decis = context.scene.panodecis
                # checkboxes
                cb_comment = context.scene.cb_comment
                cb_panostyle = context.scene.cb_panostyle
                cb_txtytz = context.scene.cb_txtytz
                cb_oxoyoz = context.scene.cb_oxoyoz
                cb_center = context.scene.cb_center
                cb_origin = context.scene.cb_origin
                cb_align = context.scene.cb_align
                cb_prealign = context.scene.cb_prealign

                usecenter = bpy.context.preferences.addons['panocamadder'].preferences.usecenter

                layout = self.layout
                col = layout.column()

                # comment
                row = layout.row()
                row.prop(context.scene, "cb_comment", text='comment')
                if cb_comment == True:
                    row.label(text=f'<!-- {obj.name} -->')

                # panostyle
                row = layout.row()
                row.prop(context.scene, "cb_panostyle", text='style')
                if cb_panostyle == True:
                    row.label(text=f'<style name="{stylename}" />')

                # txtytz
                row = layout.row()
                row.prop(context.scene, "cb_txtytz", text='tx ty tz')
                if cb_txtytz == True:
                    row.label(
                        text=f'tx="{get_krp_loc(obj,decis)[0]}" ty="{get_krp_loc(obj,decis)[1]}" tz="{get_krp_loc(obj,decis)[2]}"')

                # oxoyoz
                row = layout.row()
                row.prop(context.scene, "cb_oxoyoz", text='ox oy oz')
                if cb_oxoyoz == True:
                    row.label(
                        text=f'ox="{get_krp_loc(obj,decis)[0]}" oy="{get_krp_loc(obj,decis)[1]}" oz="{get_krp_loc(obj,decis)[2]}"')

                # origin
                row = layout.row()
                row.prop(context.scene, "cb_origin", text='origin')
                if cb_origin == True:
                    row.label(
                        text=f'origin="{get_krp_center(obj, decis)[2]}, {get_krp_center(obj, decis)[1]}, {get_krp_center(obj, decis)[0] * -1}"')

                # center
                if usecenter == True:
                    row = layout.row()
                    row.prop(context.scene, "cb_center", text='center')
                    if cb_center == True:
                        row.label(
                            text=f'center="{get_krp_center(obj, decis)[0]}, {get_krp_center(obj, decis)[1]}, {get_krp_center(obj, decis)[2]}"')

                # align
                row = layout.row()
                row.prop(context.scene, "cb_align", text='align')
                if cb_align == True:
                    row.label(
                        text=f'align="{get_krp_align(obj, decis)[0]}|{get_krp_align(obj, decis)[1]}|{get_krp_align(obj, decis)[2]}"')

                # prealign
                row = layout.row()
                row.prop(context.scene, "cb_prealign", text='prealign')
                if cb_prealign == True:
                    row.label(
                        text=f'prealign="{get_krp_prealign(obj, decis)[0]}|{get_krp_prealign(obj, decis)[1]}|{get_krp_prealign(obj, decis)[2]}"')

                layout = self.layout
                col = layout.column()
                col.scale_y = 1.3
                col.operator("pcaplus.printpano", icon='CONSOLE')
                row = layout.row()
                row.prop(context.scene, "panodecis", text='Decimals')
                row.prop(context.scene, "cb_json", text='JSON')
                row.prop(context.scene, "cb_pcijson", text='PCi-JSON')
            else:
                layout = self.layout
                col = layout.column()
                col.label(text='No MESH or EMPTY selected..')
        else:
            layout = self.layout
            col = layout.column()
            col.label(text='No MESH or EMPTY selected..')

       # HotspotValue Panel


class PCAPLUS_PT_krpanohotspot(bpy.types.Panel):

    bl_label = "Hotspot"
    bl_idname = "PCAPLUSKRPANOHS_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUSKRPANO_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        obj = bpy.context.active_object

        imagehsfolder = bpy.context.preferences.addons['panocamadder'].preferences.imagehsfolder
        modelhsfolder = bpy.context.preferences.addons['panocamadder'].preferences.modelhsfolder

        hstype = context.scene.hs_type
        decis = context.scene.hsdecis

        cb_comment = context.scene.cb_comment
        cb_hsbrackets = context.scene.cb_hsbrackets
        cb_hsname = context.scene.cb_hsname
        cb_hstype = context.scene.cb_hstype
        cb_hsstyle = context.scene.cb_hsstyle
        cb_hs_basics = context.scene.cb_hs_basics
        cb_hsloc = context.scene.cb_hsloc
        cb_hsrot = context.scene.cb_hsrot
        cb_wh = context.scene.cb_wh
        cb_roundedge = context.scene.cb_roundedge
        cb_scale = context.scene.cb_scale
        cb_bgcolor = context.scene.cb_bgcolor
        cb_alpha = context.scene.cb_alpha
        cb_imgurl = context.scene.cb_imgurl
        cb_modelurl = context.scene.cb_modelurl
        hstype = context.scene.hs_type
        model_type = context.scene.model_type

        lightmodes = ['SPOT', 'SUN', 'POINT']

        cb_hslight_name = context.scene.cb_hslight_name
        cb_hslight_loc = context.scene.cb_hslight_loc
        cb_hslight_col = context.scene.cb_hslight_col
        cb_hslight_target = context.scene.cb_hslight_target
        cb_hslight_energy = context.scene.cb_hslight_energy
        cb_hslight_mode = context.scene.cb_hslight_mode
        cb_hsbrackets = context.scene.cb_hsbrackets
        cb_hslight_spotsize = context.scene.cb_hslight_spotsize
        cb_hslight_spotblend = context.scene.cb_hslight_spotblend
        cb_hslight_shadow = context.scene.cb_hslight_shadow
        cb_hslight_distance = context.scene.cb_hslight_distance

        hs_basic_2d = bpy.context.preferences.addons['panocamadder'].preferences.hs_basic_2d
        hs_basic_3d = bpy.context.preferences.addons['panocamadder'].preferences.hs_basic_3d
        hs_basic_light = bpy.context.preferences.addons['panocamadder'].preferences.hs_basic_light

        # EMPTY
        if obj != None and obj.type == 'EMPTY':

            layout = self.layout

            # comment
            row = layout.row()
            row.prop(context.scene, "cb_comment", text='comment')
            if cb_comment == True:
                row.label(text=f'<!-- Name={obj.name} | Type={obj.type} -->')
            # hsbrackets
            row = layout.row()
            row.prop(context.scene, "cb_hsbrackets", text='<hotspot/>')
            if cb_hsbrackets == True:
                row.label(text=f'<hotspot name="{obj.name}" ... />')

            # name
            if cb_hsbrackets == False:
                row = layout.row()
                row.prop(context.scene, "cb_hsname", text='name')
                if cb_hsname == True:
                    row.label(text=f'    name="{obj.name}" ')
            # style
            row = layout.row()
            row.prop(context.scene, "cb_hsstyle", text='style')
            if cb_hsstyle == True:
                row.prop(context.scene, "stylename", text='')

            # location
            row = layout.row()
            row.prop(context.scene, "cb_hsloc", text='tx ty tz')
            if cb_hsloc == True:
                row.label(
                    text=f'tx="{get_krp_loc(obj,decis)[0]}" ty="{get_krp_loc(obj,decis)[1]}" tz="{get_krp_loc(obj,decis)[2]}"')

            # rotation
            row = layout.row()
            row.prop(context.scene, "cb_hsrot", text='rx ry rz')
            if cb_hsrot == True:
                row.label(
                    text=f'rx="{get_krp_rot_3d(obj,decis)[0]}" ry="{get_krp_rot_3d(obj,decis)[1]}" rz="{get_krp_rot_3d(obj,decis)[2]}"')

            # scale
            row = layout.row()
            row.prop(context.scene, "cb_scale", text='scale')
            if cb_scale == True:
                row.label(
                    text=f'scalex="{get_krp_scale_3d(obj,decis)[0]}" scaley="{get_krp_scale_3d(obj,decis)[1]}" scalez="{get_krp_scale_3d(obj,decis)[2]}"')

            # modelurl
            row = layout.row()
            row.prop(context.scene, "cb_modelurl", text='url')
            if cb_modelurl == True:
                row.label(text=f'url="{modelhsfolder}{obj.name}{model_type}"')
                row.prop(context.scene, "model_type", text='')

            layout = self.layout
            col = layout.column()
            col.scale_y = 1.3
            col.operator("pcaplus.prinths3d", icon='CONSOLE')
            row = layout.row()
            row.prop(context.scene, "hsdecis", text='Decimals')
            row.prop(context.scene, "cb_json", text='JSON')

        # MESH
        elif obj != None and obj.type == 'MESH':

            layout = self.layout
            col = layout.column()

            # centerorigin
            if hstype != "3D":
                col.operator("pcaplus.centerorigin", icon='SNAP_FACE_CENTER')
                col.label(text="")

            # hstype
            col.prop(context.scene, "hs_type", text='')

            # comment
            row = layout.row()
            row.prop(context.scene, "cb_comment", text='comment')
            if cb_comment == True:
                row.label(text=f'<!-- Name={obj.name} | Type={obj.type} -->')
            # hsbrackets
            row = layout.row()
            row.prop(context.scene, "cb_hsbrackets", text='<hotspot/>')
            if cb_hsbrackets == True:
                row.label(text=f'<hotspot name="{obj.name}" ... />')

            # name
            if cb_hsbrackets == False:
                row = layout.row()
                row.prop(context.scene, "cb_hsname", text='name')
                if cb_hsname == True:
                    row.label(text=f'    name="{obj.name}" ')

            # basics
            row = layout.row()
            row.prop(context.scene, "cb_hs_basics", text='basic settings')
            if cb_hs_basics == True:
                if hstype != "3D":
                    row.label(text=f'{hs_basic_2d}')
                if hstype == "3D":
                    row.label(text=f'{hs_basic_3d}')

            # type
            if hstype != "3D":
                row = layout.row()
                row.prop(context.scene, "cb_hstype", text='type')
                if cb_hstype == True:
                    row.label(text=f'    type="{hstype}" ')

            # style
            row = layout.row()
            row.prop(context.scene, "cb_hsstyle", text='style')
            if cb_hsstyle == True:
                row.prop(context.scene, "stylename", text='')

            # location
            row = layout.row()
            row.prop(context.scene, "cb_hsloc", text='tx ty tz')
            if cb_hsloc == True:
                row.label(
                    text=f'tx="{get_krp_loc(obj,decis)[0]}" ty="{get_krp_loc(obj,decis)[1]}" tz="{get_krp_loc(obj,decis)[2]}"')

            # rotation
            row = layout.row()
            row.prop(context.scene, "cb_hsrot", text='rx ry rz')
            if cb_hsrot == True:
                if hstype != "3D":
                    row.label(
                        text=f'rx="{get_krp_rot(obj,decis)[0]}" ry="{get_krp_rot(obj,decis)[1]}" rz="{get_krp_rot(obj,decis)[2]}"')
                if hstype == "3D":
                    row.label(
                        text=f'rx="{get_krp_rot_3d(obj,decis)[0]}" ry="{get_krp_rot_3d(obj,decis)[1]}" rz="{get_krp_rot_3d(obj,decis)[2]}"')

            # width/heigth
            if hstype != "3D":
                row = layout.row()
                row.prop(context.scene, "cb_wh", text='width heigth')
                if cb_wh == True:
                    row.label(
                        text=f'width="{get_krp_wh(obj)[0]}" height="{get_krp_wh(obj)[1]}"')

            # roundedge
            if hstype == 'text':
                row = layout.row()
                row.prop(context.scene, "cb_roundedge", text='roundedge')
                if cb_roundedge == True:
                    row.prop(context.scene, "roundedge", text='')

            # scale
            if hstype != "3D":
                row = layout.row()
                row.prop(context.scene, "cb_scale", text='scale')
                if cb_scale == True:
                    row.label(text=f'scale="{get_krp_scale(obj,decis)}"')
            # scale 3D
            if hstype == "3D":
                row = layout.row()
                row.prop(context.scene, "cb_scale", text='scale')
                if cb_scale == True:
                    row.label(
                        text=f'scalex="{get_krp_scale_3d(obj,decis)[0]}" scaley="{get_krp_scale_3d(obj,decis)[1]}" scalez="{get_krp_scale_3d(obj,decis)[2]}"')

            # modelurl
            if hstype == '3D':
                row = layout.row()
                row.prop(context.scene, "cb_modelurl", text='url')
                if cb_modelurl == True:
                    row.label(
                        text=f'url="{modelhsfolder}{obj.name}{model_type}"')
                    row.prop(context.scene, "model_type", text='')
            # bgcolor
            if hstype == 'text':
                for s in obj.material_slots:
                    if s.material and s.material.use_nodes:
                        for rgbn in s.material.node_tree.nodes:
                            if rgbn.name == 'pca-hscolor':
                                row = layout.row()
                                row.prop(context.scene, "cb_bgcolor",
                                         text='bgcolor:')
                                if cb_bgcolor == True:
                                    color = rgbn.outputs[0]
                                    row.prop(color, "default_value", text="")
            # alpha
            if hstype != "3D":
                for s in obj.material_slots:
                    if s.material and s.material.use_nodes:
                        for n in s.material.node_tree.nodes:
                            if n.name == 'pca-hsalpha-mixer':
                                row = layout.row()
                                row.prop(context.scene,
                                         "cb_alpha", text='alpha:')
                                if cb_alpha == True:
                                    color = n.inputs[0]
                                    row.prop(color, "default_value", text="")

            # imgurl
            if hstype == 'image':
                row = layout.row()
                row.prop(context.scene, "cb_imgurl", text='url')
                if cb_imgurl == True:
                    if imagehsfolder != '':
                        row.label(
                            text=f'url="{imagehsfolder}{get_pca_img_texture(obj)}"')
                    else:
                        row.label(text=f'url="{get_pca_img_texture(obj)}"')

            layout = self.layout
            col = layout.column()
            col.scale_y = 1.3
            if hstype != "3D":
                col.operator("pcaplus.prinths", icon='CONSOLE')
            else:
                col.operator("pcaplus.prinths3d", icon='CONSOLE')
            row = layout.row()
            row.prop(context.scene, "hsdecis", text='Decimals')
            row.prop(context.scene, "cb_json", text='JSON')

        # LIGHTSPOTS
        elif obj != None and obj.type == 'LIGHT' and obj.data.type in lightmodes:

            layout = self.layout
            col = layout.column()
            if obj.data.type == 'SPOT':
                col.label(text="Spot Light Hotspot", icon="LIGHT_SPOT")
            if obj.data.type == 'SUN':
                col.label(text="Sun Light Hotspot", icon="LIGHT_SUN")
            if obj.data.type == 'POINT':
                col.label(text="Point Light Hotspot", icon="LIGHT_POINT")

            # comment
            row = layout.row()
            row.prop(context.scene, "cb_comment", text='comment')
            if cb_comment == True:
                row.scale_x = 0.4
                row.label(text='')
                row.scale_x = 1.6
                row.label(text=f'<!-- Name={obj.name} | Type={obj.type} -->')

            # hsbrackets
            row = layout.row()
            row.prop(context.scene, "cb_hsbrackets", text='<hotspot/>')
            if cb_hsbrackets == True:
                row.scale_x = 0.4
                row.label(text='')
                row.scale_x = 1.6
                row.label(text=f'<hotspot ... />')

            # name
            row = layout.row()
            row.prop(context.scene, "cb_hslight_name", text='name')
            if cb_hslight_name == True:
                row.scale_x = 0.4
                row.label(text='')
                row.scale_x = 1.6
                row.label(text=f'name="{obj.name}"')

            # basics
            row = layout.row()
            row.prop(context.scene, "cb_hs_basics", text='basic settings')
            if cb_hs_basics == True:
                row.label(text=f'{hs_basic_light}')

            # style
            row = layout.row()
            row.prop(context.scene, "cb_hsstyle", text='style')
            if cb_hsstyle == True:
                if obj.data.type == "SPOT":
                    row.scale_x = 0.4
                    row.label(text='')
                    row.scale_x = 1.6
                    row.prop(context.scene, "stylespot", text='')
                if obj.data.type == "SUN":
                    row.scale_x = 0.4
                    row.label(text='')
                    row.scale_x = 1.6
                    row.prop(context.scene, "stylesun", text='')
                if obj.data.type == "POINT":
                    row.scale_x = 0.4
                    row.label(text='')
                    row.scale_x = 1.6
                    row.prop(context.scene, "stylepoint", text='')

            # mode
            row = layout.row()
            row.prop(context.scene, "cb_hslight_mode", text='mode')
            if cb_hslight_mode == True:
                row.scale_x = 0.4
                row.label(text='')
                row.scale_x = 1.6
                row.label(text=f'mode="{obj.data.type.lower()}"')

            # location
            row = layout.row()
            row.prop(context.scene, "cb_hslight_loc", text='location')
            if cb_hslight_loc == True:
                if obj.data.type == 'SPOT' or obj.data.type == 'POINT':
                    row.scale_x = 0.4
                    row.label(text='')
                    row.scale_x = 1.6
                    row.label(
                        text=f'tx="{get_krp_loc(obj,decis)[0]}" ty="{get_krp_loc(obj,decis)[1]}" tz="{get_krp_loc(obj,decis)[2]}"')

                if obj.data.type == 'SUN':
                    row.scale_x = 0.4
                    row.label(text='')
                    row.scale_x = 1.6
                    row.label(
                        text=f'ath="{get_krp_sunpos(obj,decis)[0]}" atv="{get_krp_sunpos(obj,decis)[1]}"')

            # distance
            if obj.data.type == 'SPOT' or obj.data.type == 'POINT':
                row = layout.row()
                row.prop(context.scene, "cb_hslight_distance", text='distance')
                if cb_hslight_distance == True:
                    row.prop(obj.data, "use_custom_distance", text="")
                    if obj.data.use_custom_distance == True:
                        row.scale_x = 0.6
                        row.prop(obj.data, "cutoff_distance", text="")
                        row.label(
                            text=f'distance="{round(obj.data.cutoff_distance * 100, decis)}"')
                    else:
                        row.scale_x = 0.6
                        row.label(text=f'distance="0"')
                        row.label(text="")

            # target
            if obj.data.type == 'SPOT':
                row = layout.row()
                row.prop(context.scene, "cb_hslight_target", text='target')
                if cb_hslight_target == True:
                    row.scale_x = 0.4
                    row.label(text='')
                    row.scale_x = 1.6
                    row.label(
                        text=f'targetx="{round(get_krp_spottarget(obj)[0], decis)}" targety="{round(get_krp_spottarget(obj)[1], decis)}" targetz="{round(get_krp_spottarget(obj)[2], decis)}')

                # spotzize
                row = layout.row()
                row.prop(context.scene, "cb_hslight_spotsize", text='angle')
                if cb_hslight_spotsize == True:
                    row.scale_x = 0.4
                    row.prop(obj.data, "spot_size", text="")
                    row.scale_x = 1.6
                    row.label(
                        text=f'angle="{round(degrees(obj.data.spot_size), decis)}"')
                # penumbra
                row = layout.row()
                row.prop(context.scene, "cb_hslight_spotblend", text='penumbra')
                if cb_hslight_spotblend == True:
                    row.scale_x = 0.4
                    row.prop(obj.data, "spot_blend", text="")
                    row.scale_x = 1.6
                    row.label(
                        text=f'penumbra="{round(obj.data.spot_blend, decis)}"')

            # energy
            row = layout.row()
            row.prop(context.scene, "cb_hslight_energy", text='intensity')
            if cb_hslight_energy == True:
                row.scale_x = 0.4
                row.prop(obj.data, "energy", text="")
                row.scale_x = 1.6
                row.label(
                    text=f'intensity="{round(obj.data.energy / 10,decis)}"')

            # color
            row = layout.row()
            row.prop(context.scene, "cb_hslight_col", text='color')
            if cb_hslight_col == True:
                row.scale_x = 0.4
                row.prop(obj.data, "color", text="")
                row.scale_x = 1.6
                row.label(
                    text=f'color="{floats_to_hex(obj.data.color[0],obj.data.color[1],obj.data.color[2])}"')

            # shadow
            row = layout.row()
            row.prop(context.scene, "cb_hslight_shadow", text='castshadow')
            if cb_hslight_shadow == True:

                row.prop(obj.data, "use_shadow", text="")
                row.scale_x = 0.6
                if obj.data.use_shadow == True:
                    row.label(text=f'castshadow="true"')
                    row.label(text="")
                else:
                    row.label(text=f'castshadow="false"')
                    row.label(text="")

            # print
            layout = self.layout
            col = layout.column()
            col.scale_y = 1.3
            col.operator("pcaplus.printhslight", icon='CONSOLE')
            row = layout.row()
            row.prop(context.scene, "hsdecis", text='Decimals')
            row.prop(context.scene, "cb_json", text='JSON')

        else:
            layout = self.layout
            col = layout.column()
            col.label(text='No MESH, LIGHT or EMPTY selected..')

    # VIEW VALUES


class PCAPLUS_PT_krpanoview(bpy.types.Panel):

    bl_label = "Camera/View"
    bl_idname = "PCAPLUSKRPANOVIEW_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUSKRPANO_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        obj = bpy.context.active_object

        # checkboxes
        cb_comment = context.scene.cb_comment
        cb_hlookat = context.scene.cb_hlookat
        cb_vlookat = context.scene.cb_vlookat
        cb_fov = context.scene.cb_fov
        cb_camtxtytz = context.scene.cb_camtxtytz
        cb_camoxoyoz = context.scene.cb_camoxoyoz
        cb_camcenter = context.scene.cb_camcenter
        cb_camorigin = context.scene.cb_camorigin

        usecenter = bpy.context.preferences.addons['panocamadder'].preferences.usecenter
        decis = context.scene.viewdecis

        if obj != None and obj.type == 'CAMERA':

            layout = self.layout

            # comment
            row = layout.row()
            row.prop(context.scene, "cb_comment", text='comment')
            if cb_comment == True:
                row.label(text=f'<!-- {obj.name} -->')
            # hlookat
            row = layout.row()
            row.prop(context.scene, "cb_hlookat", text='hlookat')
            if cb_hlookat == True:
                row.label(text=f'hlookat="{get_krp_lookat(obj, decis)[0]}"')
            # vlookat
            row = layout.row()
            row.prop(context.scene, "cb_vlookat", text='vlookat')
            if cb_vlookat == True:
                row.label(text=f'vlookat="{get_krp_lookat(obj, decis)[1]}"')
            # fov
            row = layout.row()
            row.prop(context.scene, "cb_fov", text='fov')
            if cb_fov == True:
                row.label(text=f'fov="{get_krp_fov(obj, decis)}"')
            # txtytz
            row = layout.row()
            row.prop(context.scene, "cb_camtxtytz", text='tx ty tz')
            if cb_camtxtytz == True:
                row.label(
                    text=f'tx="{get_krp_loc(obj,decis)[0]}" ty="{get_krp_loc(obj,decis)[1]}" tz="{get_krp_loc(obj,decis)[2]}"')

            # oxoyoz
            row = layout.row()
            row.prop(context.scene, "cb_camoxoyoz", text='ox oy oz')
            if cb_camoxoyoz == True:
                row.label(
                    text=f'ox="{get_krp_loc(obj,decis)[0]}" oy="{get_krp_loc(obj,decis)[1]}" oz="{get_krp_loc(obj,decis)[2]}"')

            # origin
            row = layout.row()
            row.prop(context.scene, "cb_camorigin", text='origin')
            if cb_camorigin == True:
                row.label(
                    text=f'origin="{get_krp_center(obj, decis)[2]}, {get_krp_center(obj, decis)[1]}, {get_krp_center(obj, decis)[0] * -1}"')

            # center
            if usecenter == True:
                row = layout.row()
                row.prop(context.scene, "cb_camcenter", text='center')
                if cb_camcenter == True:
                    row.label(
                        text=f'center="{get_krp_center(obj, decis)[0]}, {get_krp_center(obj, decis)[1]}, {get_krp_center(obj, decis)[2]}"')

            layout = self.layout
            col = layout.column()
            col.scale_y = 1.3
            col.operator("pcaplus.printview", icon='CONSOLE')
            row = layout.row()
            row.prop(context.scene, "viewdecis", text='Decimals')
            row.prop(context.scene, "cb_json", text='JSON')
        else:
            layout = self.layout
            col = layout.column()
            col.label(text='No CAMERA selected..')

      # Dollhouse Texture Panel


class PCAPLUS_PT_dollhouse(bpy.types.Panel):
    """Create Dollhouse Texture"""
    bl_label = "Dollhouse Texture / Baking"
    bl_idname = "PCAPLUSDOLLHOUSE_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUS_PT_Main'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        if context.mode == 'OBJECT':

            cb_anglebased = context.scene.cb_anglebased

            layout = self.layout
            box = layout.box()
            col = box.column(align=True)
            col.prop(context.scene, "cb_protectfacemask",
                     text='Protect Vertex Group')
            row = box.row()
            row.prop(context.scene, "cb_anglebased", text='Angle-based')

            if cb_anglebased:
                row.prop(context.scene, "anglemaxdist", text='max distance')

            col = box.column()
            col.operator("pcaplus.dollhousetexture", icon='MATERIAL_DATA')

        else:
            layout = self.layout
            box = layout.box()
            box.label(text=" Switch to object-mode")

      # DollhouseInfo Panel


class PCAPLUS_PT_dollhousebake(bpy.types.Panel):

    bl_label = "Bake"
    bl_idname = "PCAPLUSDOLLHOUSEBAKE_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUSDOLLHOUSE_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        # bake
        if context.mode == 'OBJECT':
            layout = self.layout
            box = layout.box()
            col = box.column(align=True)
            col.prop(context.scene, "cb_createuv", text='Create UV')
            col.prop(context.scene, "bakeimgname", text='')
            col.prop(context.scene, "bakeimgsize", text='')

            col = box.column()
            col.operator("pcaplus.dollhousebake", icon='IMAGE_DATA')
        else:
            layout = self.layout
            box = layout.box()
            box.label(text=" Switch to object-mode")

      # Polygonspot Panel


class PCAPLUS_PT_dollhouseinfo(bpy.types.Panel):

    bl_label = "info"
    bl_idname = "PCAPLUSDOLLHOUSEINFO_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUSDOLLHOUSE_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout
        col = layout.column(align=True)
        col.label(text="1: Select one ore more '_HANDLE'  and the model")
        col.label(text="2: Keep sure model is active object!")
        col.label(text="3: Click 'distribute..' or 'bake..'")


class PCAPLUS_PT_krpanopolyspot(bpy.types.Panel):

    bl_label = "Polygon-Hotspots"
    bl_idname = "PCAPLUSKRPANOPOLYSPOT_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUS_PT_Main'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        if bpy.context.active_object != None and bpy.context.active_object.type == 'MESH':

            cb_poly_comment = context.scene.cb_poly_comment
            obj = bpy.context.active_object

            layout = self.layout
            row = layout.row()
            row.label(text="Name:")
            row.prop(context.scene, "pgname", text='')

            row = layout.row()
            row.label(text="Style:")
            row.prop(context.scene, "pgstyle", text='')

            row = layout.row()
            row.prop(context.scene, "cb_poly_comment", text='comment')
            if cb_poly_comment == True:
                row.label(text=f'<!-- Object: {obj.name} -->')

            col = layout.column()
            col.prop(context.scene, "cb_json", text='JSON')
            col.operator("pca.printpolypoints",
                         text="Print Points3D", icon='OUTLINER_OB_POINTCLOUD')

        else:
            layout = self.layout
            row = layout.row()
            row.label(text=f"No MESH selected")

      # MESHSPLITTER Panel


class PCAPLUS_PT_krpanopolysplit(bpy.types.Panel):

    bl_label = "MeshSplitter"
    bl_idname = "PCAPLUSKRPANOPOLYSPLIT_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUSKRPANOPOLYSPOT_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        if bpy.context.active_object != None and bpy.context.active_object.type == 'MESH':

            obj = bpy.context.active_object
            faces = len(obj.data.polygons)

            layout = self.layout
            row = layout.row()
            col = layout.column()
            col.label(text=f"Object: {obj.name} ({faces} polygons)")
            col.operator("pca.facesplitter",
                         text="Split Mesh", icon='AXIS_TOP')
        else:
            layout = self.layout
            row = layout.row()
            row.label(text=f"select a mesh")

    # PanoRenderer Panel


class PCAPLUS_PT_panorenderer(bpy.types.Panel):
    """Render Panoramas"""
    bl_label = "Panorama Renderer"
    bl_idname = "PCAPLUSRENDER_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PCA+"
    bl_parent_id = 'PCAPLUS_PT_Main'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        # name
        row = layout.row()
        row.label(text="Name:")
        row.prop(context.scene, "pname", text='')

        # rendersize
        row = layout.row()
        row.label(text="Size:")
        row.prop(context.scene, "rendersize", text='')

        # north
        row = layout.row()
        row.label(text="North:")
        row.prop(context.scene, "cb_north", text='')

        # animation
        row = layout.row()
        row.label(text="Animation (image sequence ):")
        row.prop(context.scene, "cb_ani", text='')

        # JSON
        row = layout.row()
        row.prop(context.scene, "cb_json", text='JSON')
        row.prop(context.scene, "cb_pcijson", text='PCi-JSON')
        row.prop(context.scene, "panodecis", text='Decimals')

        # render BTN
        col = layout.column()
        col.scale_y = 1.5
        col.operator("pca.panorender", text="Render", icon='RENDERLAYERS')
