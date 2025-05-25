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
from . pca_prefs import PCA_Preferences
from . pca_settings import PCAsettings
from . pca_ui import PCAPLUS_PT_main, PCAPLUS_PT_pcimporter, PCAPLUS_PT_krptoblender, PCAPLUS_PT_camera, PCAPLUS_PT_viewport, PCAPLUS_PT_helpers, PCAPLUS_PT_helpermaterials, PCAPLUS_PT_export, PCAPLUS_PT_exportinfo, PCAPLUS_PT_krpano, PCAPLUS_PT_krpanodepthpano, PCAPLUS_PT_krpanohotspot, PCAPLUS_PT_krpanoview, PCAPLUS_PT_dollhouse, PCAPLUS_PT_dollhousebake, PCAPLUS_PT_dollhouseinfo, PCAPLUS_PT_krpanopolyspot, PCAPLUS_PT_krpanopolysplit, PCAPLUS_PT_panorenderer
from . pca_op_loadpcijson import PCA_OT_loadpcijson
from . pca_op_createpci import PCA_OT_createallpci, PCA_OT_createsinglepci
from . pca_op_addpc import PCAPLUS_OT_addpcop
from . pca_op_addhs import PCAPLUS_OT_addhsop
from . pca_op_addhsi import PCAPLUS_OT_addhsiop
from . pca_op_camviews import PCAPLUS_OT_downcam, PCAPLUS_OT_horizoncam, PCAPLUS_OT_look360cam, PCAPLUS_OT_topcam
from . pca_op_mats import PCAPLUS_OT_depthmat, PCAPLUS_OT_uvmat, PCAPLUS_OT_checkmat
from . pca_op_krptob import PCAPLUS_OT_torxryrz, PCAPLUS_OT_todcenter, PCAPLUS_OT_tooxoyoz, PCAPLUS_OT_toprealign
from . pca_op_depthmodel import PCAPLUS_OT_depthmodel
from . pca_op_hsprinter import PCAPLUS_OT_prinths, PCAPLUS_OT_centerorigin
from . pca_op_hs3dprinter import PCAPLUS_OT_prinths3d
from . pca_op_hslight_printer import PCAPLUS_OT_printhslight
from . pca_op_panoprinter import PCAPLUS_OT_printpano
from . pca_op_viewprinter import PCAPLUS_OT_printview
from . pca_op_polyprint import PCA_OT_printpolypoints
from . pca_op_meshsplitter import PCA_OT_facesplitter
from . pca_op_panorenderer import PCA_OT_panorender
from . pca_op_dollhouse import PCAPLUS_OT_dollhousetexture, PCAPLUS_OT_dollhousebake


bl_info = {
    "name": "PanoCamAdder",
    "author": "DerMische",
    "version": (2, 3, 0),
    "blender": (4, 3, 0),
    "location": "View3D > UI > PCA+",
    "description": "360° Panorama toolbox for KRPano 3D-depthmap-tours",
    "warning": "",
    "doc_url": "https://der-mische.de/panocamadder/",
    "category": "3D View",
}


classes = (PCA_Preferences,
           PCAsettings,
           PCAPLUS_PT_main,
           PCAPLUS_PT_pcimporter,
           PCAPLUS_PT_krptoblender,
           PCAPLUS_PT_camera,
           PCAPLUS_PT_helpers,
           PCAPLUS_PT_helpermaterials,
           PCAPLUS_PT_viewport,
           PCAPLUS_PT_export,
           PCAPLUS_PT_exportinfo,
           PCAPLUS_PT_krpano,
           PCAPLUS_PT_krpanodepthpano,
           PCAPLUS_PT_krpanohotspot,
           PCAPLUS_PT_krpanoview,
           PCAPLUS_PT_dollhouse,
           PCAPLUS_PT_dollhousebake,
           PCAPLUS_PT_dollhouseinfo,
           PCAPLUS_PT_krpanopolyspot,
           PCAPLUS_PT_krpanopolysplit,
           PCAPLUS_PT_panorenderer,
           PCA_OT_loadpcijson,
           PCA_OT_createallpci,
           PCA_OT_createsinglepci,
           PCAPLUS_OT_addpcop,
           PCAPLUS_OT_addhsop,
           PCAPLUS_OT_addhsiop,
           PCAPLUS_OT_downcam,
           PCAPLUS_OT_horizoncam,
           PCAPLUS_OT_look360cam,
           PCAPLUS_OT_topcam,
           PCAPLUS_OT_depthmat,
           PCAPLUS_OT_uvmat,
           PCAPLUS_OT_checkmat,
           PCAPLUS_OT_torxryrz,
           PCAPLUS_OT_todcenter,
           PCAPLUS_OT_tooxoyoz,
           PCAPLUS_OT_toprealign,
           PCAPLUS_OT_depthmodel,
           PCAPLUS_OT_prinths,
           PCAPLUS_OT_prinths3d,
           PCAPLUS_OT_printhslight,
           PCAPLUS_OT_centerorigin,
           PCAPLUS_OT_printpano,
           PCAPLUS_OT_printview,
           PCA_OT_printpolypoints,
           PCA_OT_facesplitter,
           PCA_OT_panorender,
           PCAPLUS_OT_dollhousetexture,
           PCAPLUS_OT_dollhousebake)


# register, unregister = bpy.utils.register_classes_factory(classes)

def register():
    addon_updater_ops.register(bl_info)
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    addon_updater_ops.unregister()
    for cls in classes:
        bpy.utils.unregister_class(cls)
