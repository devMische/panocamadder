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
from . import addon_updater_ops


class PCA_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    imagehsfolder: bpy.props.StringProperty(
        name="imagehsfolder", description="your folder for image hotspots", default='images/')  # type: ignore
    modelhsfolder: bpy.props.StringProperty(
        name="modelhsfolder", description="your folder for 3D hotspots", default='models/')  # type: ignore
    usecenter: bpy.props.BoolProperty(
        name="usecenter", default=False)  # type: ignore
    uselinkedscene: bpy.props.BoolProperty(
        name="uselinkedscene", default=True)  # type: ignore
    nomatcolor: bpy.props.FloatVectorProperty(
        name="nomatcolor", description="color for the noMAT.", subtype="COLOR", size=4, default=(1, 0, 0.5, 1))  # type: ignore
    xmatcolor: bpy.props.FloatVectorProperty(
        name="xmatcolor", description="color for the xMAT.", subtype="COLOR", size=4, default=(1, 1, 0.0, 1))  # type: ignore

    hs_basic_2d: bpy.props.StringProperty(name="hs_basic_2d", description="basic settings",
                                          default='distorted="true" keep="true" depth="0" depthbuffer="true" rotationorder="xzy" enabled="true" capture="false"')  # type: ignore
    hs_basic_3d: bpy.props.StringProperty(
        name="hs_basic_3d", description="basic settings", default=' keep="true"')  # type: ignore
    hs_basic_light: bpy.props.StringProperty(
        name="hs_basic_light", description="basic settings", default='type="threejslight" keep="true"')  # type: ignore

    pano_extension: bpy.props.StringProperty(
        name="pano_extension", description="panoimage extension", default='jpg')  # type: ignore
    renderpano_extension: bpy.props.StringProperty(
        name="renderpano_extension", description="renderpano extension", default='jpg')  # type: ignore

    auto_check_update: bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False)  # type: ignore

    updater_interval_months: bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0)  # type: ignore

    updater_interval_days: bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31)  # type: ignore

    updater_interval_hours: bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23)  # type: ignore

    updater_interval_minutes: bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59)  # type: ignore

    def draw(self,  context):
        layout = self.layout
        box = layout.box()
        box.label(text="KRPANO Values")
        col = box.column(align=True)
        col.label(text="Hotspot:")
        col.prop(self, 'imagehsfolder', text="image hotspot folder")
        col.prop(self, 'modelhsfolder', text="3D hotspot folder")
        col.prop(self, 'hs_basic_2d', text="text/image-hotspot basics")
        col.prop(self, 'hs_basic_3d', text="3D-hotspot basics")
        col.prop(self, 'hs_basic_light', text="light-hotspot basics")

        layout.separator()

        col = box.column(align=True)
        col.separator(factor=1.0, type='LINE')
        col.label(text="Depthmap/Panorama:")
        col.prop(self, 'uselinkedscene', text="print linkedscene")
        col.prop(self, 'usecenter', text="show depthmap.center (outdated)")
        col.prop(self, 'pano_extension', text="pano image extension")

        layout.separator()

        col = box.column(align=True)
        col.separator(factor=1.0, type='LINE')
        col.label(text="Panorenderer:")
        col.prop(self, 'renderpano_extension',
                 text="renderpano image extension")

        box = layout.box()
        box.label(text="Distribute PanoMATs:")
        col = box.column(align=True)
        col.prop(self, 'nomatcolor', text="no_MAT color")
        col.prop(self, 'xmatcolor', text="x_MAT color")

        layout.separator()

        layout = self.layout
        # Works best if a column, or even just self.layout.
        mainrow = layout.row()
        col = mainrow.column()

        # Updater draw function, could also pass in col as third arg.
        addon_updater_ops.update_settings_ui(self, context)
