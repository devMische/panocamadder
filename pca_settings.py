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


class PCAsettings(bpy.types.PropertyGroup):

    # material/world checkboxes
    bpy.types.Scene.cb_matworld = bpy.props.BoolProperty(
        name="matworld", description="Apply material to the selected mesh", default=True)
    bpy.types.Scene.cb_protectfacemask = bpy.props.BoolProperty(
        name="protectfacemask", description="Exclude selected vertex group", default=False)

    # pano checkboxes
    bpy.types.Scene.cb_comment = bpy.props.BoolProperty(
        name="comment", default=True)
    bpy.types.Scene.cb_panostyle = bpy.props.BoolProperty(
        name="cb_panostyle", default=True)
    bpy.types.Scene.cb_txtytz = bpy.props.BoolProperty(
        name="txtytz", default=True)
    bpy.types.Scene.cb_oxoyoz = bpy.props.BoolProperty(
        name="oxoyoz", default=True)
    bpy.types.Scene.cb_center = bpy.props.BoolProperty(
        name="center", default=True)
    bpy.types.Scene.cb_origin = bpy.props.BoolProperty(
        name="origin", default=True)
    bpy.types.Scene.cb_align = bpy.props.BoolProperty(
        name="align", default=True)
    bpy.types.Scene.cb_prealign = bpy.props.BoolProperty(
        name="prealign", default=True)
    bpy.types.Scene.cb_tourmodel = bpy.props.BoolProperty(
        name="cb_tourmodel",
        description="Create an arrangement with all well aligned Depth-Models",
        default=True)

    # cam checkboxes
    bpy.types.Scene.cb_hlookat = bpy.props.BoolProperty(
        name="hlookat", default=True)
    bpy.types.Scene.cb_vlookat = bpy.props.BoolProperty(
        name="vlookat", default=True)
    bpy.types.Scene.cb_fov = bpy.props.BoolProperty(name="fov", default=True)
    bpy.types.Scene.cb_camtxtytz = bpy.props.BoolProperty(
        name="camtxtytz", default=True)
    bpy.types.Scene.cb_camoxoyoz = bpy.props.BoolProperty(
        name="camoxoyoz", default=True)
    bpy.types.Scene.cb_camcenter = bpy.props.BoolProperty(
        name="camcenter", default=True)
    bpy.types.Scene.cb_camorigin = bpy.props.BoolProperty(
        name="camorigin", default=True)

    # HS checkboxes
    bpy.types.Scene.cb_hsbrackets = bpy.props.BoolProperty(
        name="hsbrackets", default=False)
    bpy.types.Scene.cb_hsname = bpy.props.BoolProperty(
        name="cb_hsname", default=False)
    bpy.types.Scene.cb_hstype = bpy.props.BoolProperty(
        name="cb_hstype", default=False)
    bpy.types.Scene.cb_hsstyle = bpy.props.BoolProperty(
        name="hsstyle", default=False)
    bpy.types.Scene.cb_hs_basics = bpy.props.BoolProperty(
        name="hs3d", default=False)
    bpy.types.Scene.cb_hsloc = bpy.props.BoolProperty(
        name="hsloc", default=True)
    bpy.types.Scene.cb_hsrot = bpy.props.BoolProperty(
        name="hsrot", default=True)
    bpy.types.Scene.cb_scale = bpy.props.BoolProperty(
        name="scale", default=True)
    bpy.types.Scene.cb_wh = bpy.props.BoolProperty(name="wh", default=True)
    bpy.types.Scene.cb_roundedge = bpy.props.BoolProperty(
        name="roundedge", default=True)
    bpy.types.Scene.cb_bgcolor = bpy.props.BoolProperty(
        name="bgcolor", default=True)
    bpy.types.Scene.cb_alpha = bpy.props.BoolProperty(
        name="alpha", default=True)
    bpy.types.Scene.cb_imgurl = bpy.props.BoolProperty(
        name="imgurl", default=True)
    bpy.types.Scene.cb_modelurl = bpy.props.BoolProperty(
        name="cb_modelurl", default=True)

    # HS POLY checkboxes
    bpy.types.Scene.cb_poly_comment = bpy.props.BoolProperty(
        name="cb_poly_comment", default=True)

    # HS-LIGHT checkboxes
    bpy.types.Scene.cb_hslight_name = bpy.props.BoolProperty(
        name="cb_hslight_name", default=True)
    bpy.types.Scene.cb_hslight_mode = bpy.props.BoolProperty(
        name="cb_hslight_mode", default=True)
    bpy.types.Scene.cb_hslight_loc = bpy.props.BoolProperty(
        name="cb_hslight_loc", default=True)
    bpy.types.Scene.cb_hslight_target = bpy.props.BoolProperty(
        name="cb_hslight_target", default=True)
    bpy.types.Scene.cb_hslight_spotsize = bpy.props.BoolProperty(
        name="cb_hslight_spotsize", default=True)
    bpy.types.Scene.cb_hslight_spotblend = bpy.props.BoolProperty(
        name="cb_hslight_spotblend", default=True)
    bpy.types.Scene.cb_hslight_col = bpy.props.BoolProperty(
        name="cb_hslight_col", default=True)
    bpy.types.Scene.cb_hslight_energy = bpy.props.BoolProperty(
        name="cb_hslight_energy", default=True)
    bpy.types.Scene.cb_hslight_shadow = bpy.props.BoolProperty(
        name="cb_hslight_shadow", default=True)
    bpy.types.Scene.cb_hslight_distance = bpy.props.BoolProperty(
        name="cb_hslight_distance", default=True)

    # dollhouse checkboxes
    bpy.types.Scene.cb_anglebased = bpy.props.BoolProperty(
        name="anglebased", default=False)
    bpy.types.Scene.anglemaxdist = bpy.props.FloatVectorProperty(
        name="anglemaxdist", description="distance to search for better angle", size=1, min=0.0, max=200.0, default=[100.0])
    bpy.types.Scene.bakeimgname = bpy.props.StringProperty(
        name="bakeimgname", description="Image name", default='MyDollhouseTexture')
    bpy.types.Scene.bakeimgsize = bpy.props.IntProperty(
        name="bakeimgsize", description="image size", min=256, default=2048)

    # uv bake checkbox
    bpy.types.Scene.cb_createuv = bpy.props.BoolProperty(
        name="createuv", description="create UV layout", default=False)

    # panorender checkbox
    bpy.types.Scene.rendertype = bpy.props.EnumProperty(
        name="",
        description="Panorama or Images",
        items=[('panorama', "Panorama", ""),
               ('images', "Images", "")
               ]
    )
    bpy.types.Scene.pname = bpy.props.StringProperty(
        name="pname", description="Give the panorama a name", default='MyPano')
    bpy.types.Scene.rendersize = bpy.props.IntProperty(
        name="rendersize", description="Size for the cubfaces - or the equirectangular width", min=0, default=512)
    bpy.types.Scene.cb_north = bpy.props.BoolProperty(
        name="cb_north", default=True)
    bpy.types.Scene.cb_ani = bpy.props.BoolProperty(
        name="cb_ani", default=False)

    # JSON output checkbox
    bpy.types.Scene.cb_json = bpy.props.BoolProperty(
        name="cb_json", description="Output JSON data", default=False)
    bpy.types.Scene.cb_pcijson = bpy.props.BoolProperty(
        name="cb_pcijson", description="Output PCi-JSON data", default=False)

    # polys props
    bpy.types.Scene.pgname = bpy.props.StringProperty(
        name="pgname", description="The name", default='PolySpot')
    bpy.types.Scene.pgstyle = bpy.props.StringProperty(
        name="pgstyle", description="The style", default='MyStyle')
    bpy.types.Scene.cb_objname = bpy.props.BoolProperty(
        name="objname", default=True)

    # HS props
    bpy.types.Scene.stylename = bpy.props.StringProperty(
        name="stylename", description="style name", default='MyStyle')
    bpy.types.Scene.hsdecis = bpy.props.IntProperty(
        name="hsdecis", description="decimals", min=1, max=8, default=2)
    bpy.types.Scene.roundedge = bpy.props.IntProperty(
        name="roundedge", description="roundedge", min=0, default=5)
    bpy.types.Scene.hs_type = bpy.props.EnumProperty(
        name="",
        description="Select Hotspot Type",
        items=[('text', "Text", ""),
               ('image', "Image", ""),
               ('3D', "3D", "")
               ]
    )

    bpy.types.Scene.model_type = bpy.props.EnumProperty(
        name="",
        description="Select Model Type",
        items=[('.obj', ".obj", ""),
               ('.glb', ".glb", ""),
               ('.gltf', ".gltf", "")
               ]
    )

    # LIGHT HS props
    bpy.types.Scene.stylesun = bpy.props.StringProperty(
        name="stylesun", description="style name", default='sunlight')
    bpy.types.Scene.stylespot = bpy.props.StringProperty(
        name="stylespot", description="style name", default='spotlight')
    bpy.types.Scene.stylepoint = bpy.props.StringProperty(
        name="stylepoint", description="style name", default='pointlight')

    # pano props
    bpy.types.Scene.panodecis = bpy.props.IntProperty(
        name="panodecis", description="decimals", min=0, max=20, default=2)
    bpy.types.Scene.viewdecis = bpy.props.IntProperty(
        name="viewdecis", description="decimals", min=1, max=10, default=2)

    # krp input code
    bpy.types.Scene.krpcode = bpy.props.StringProperty(
        name="krpcode", description='Insert (pre)align, ox/oy/oz, tx/ty/oz, rx/ry/rz, origin or center')

    # PCI
    bpy.types.Scene.jsonfile = ""
    bpy.types.Scene.jsonpath = ""
    bpy.types.Scene.jsondata = []
    bpy.types.Scene.pcijson = []
    bpy.types.Scene.panos = []
    bpy.types.Scene.panonmbr = bpy.props.IntProperty(name="panonmbr",
                                                     description="panonmbr",
                                                     min=1,
                                                     max=1,
                                                     default=1)

    # PCi props
    bpy.types.Scene.rad_or_deg = bpy.props.EnumProperty(
        name="rad_or_deg",
        description="Is rotation input in radians or degrees",
        default="radians",
        items=[('radians', "radians", ""),
               ('degrees', "degrees", "")
               ]
    )

    bpy.types.Scene.cb_radians = bpy.props.BoolProperty(
        name="cb_radians",
        default=False,
        description="use radians instead of degrees")

    bpy.types.Scene.json_loc_x = bpy.props.EnumProperty(
        name="json_loc_x",
        description="Select Axis",
        default="0",
        items=[('0', "location[0]", ""),
               ('1', "location[1]", ""),
               ('2', "location[2]", "")
               ]
    )

    bpy.types.Scene.json_loc_y = bpy.props.EnumProperty(
        name="json_loc_y",
        description="Select Axis",
        default="1",
        items=[('0', "location[0]", ""),
               ('1', "location[1]", ""),
               ('2', "location[2]", "")
               ]
    )

    bpy.types.Scene.json_loc_z = bpy.props.EnumProperty(
        name="json_loc_z",
        description="Select Axis",
        default="2",
        items=[('0', "location[0]", ""),
               ('1', "location[1]", ""),
               ('2', "location[2]", "")
               ]
    )

    bpy.types.Scene.loc_x_operator = bpy.props.EnumProperty(
        name="Select Operator",
        default="no",
        items=[('no', "no math", ""),
               ('+', "+", ""),
               ('-', "-", ""),
               ('*', "*", ""),
               ('/', "/", "")
               ]
    )

    bpy.types.Scene.loc_y_operator = bpy.props.EnumProperty(
        name="Select Operator",
        default="no",
        items=[('no', "no math", ""),
               ('+', "+", ""),
               ('-', "-", ""),
               ('*', "*", ""),
               ('/', "/", "")
               ]
    )

    bpy.types.Scene.loc_z_operator = bpy.props.EnumProperty(
        name="Select Operator",
        default="no",
        items=[('no', "no math", ""),
               ('+', "+", ""),
               ("-", "-", ""),
               ("*", "*", ""),
               ("/", "/", "")
               ]
    )

    bpy.types.Scene.loc_x_nmbr = bpy.props.FloatProperty(
        name="loc_x_nmbr", description="number")
    bpy.types.Scene.loc_y_nmbr = bpy.props.FloatProperty(
        name="loc_y_nmbr", description="number")
    bpy.types.Scene.loc_z_nmbr = bpy.props.FloatProperty(
        name="loc_z_nmbr", description="number")

    bpy.types.Scene.json_rot_x = bpy.props.EnumProperty(
        name="json_rot_x",
        description="Select Axis",
        default="0",
        items=[('0', "rotation[0]", ""),
               ('1', "rotation[1]", ""),
               ('2', "rotation[2]", "")
               ]
    )

    bpy.types.Scene.json_rot_y = bpy.props.EnumProperty(
        name="json_rot_y",
        description="Select Axis",
        default="1",
        items=[('0', "rotation[0]", ""),
               ('1', "rotation[1]", ""),
               ('2', "rotation[2]", "")
               ]
    )

    bpy.types.Scene.json_rot_z = bpy.props.EnumProperty(
        default="2",
        description="Select Axis",
        items=[('0', "rotation[0]", ""),
               ('1', "rotation[1]", ""),
               ('2', "rotation[2]", "")
               ]
    )

    bpy.types.Scene.rot_x_operator = bpy.props.EnumProperty(
        default="no",
        name="Select Operator",
        items=[('no', "no math", ""),
               ('+', "+", ""),
               ("-", "-", ""),
               ("*", "*", ""),
               ("/", "/", "")
               ]
    )

    bpy.types.Scene.rot_y_operator = bpy.props.EnumProperty(
        name="Select Operator",
        default="no",
        items=[('no', "no math", ""),
               ('+', "+", ""),
               ("-", "-", ""),
               ("*", "*", ""),
               ("/", "/", "")
               ]
    )

    bpy.types.Scene.rot_z_operator = bpy.props.EnumProperty(
        name="Select Operator",
        default="no",
        items=[('no', "no math", ""),
               ('+', "+", ""),
               ("-", "-", ""),
               ("*", "*", ""),
               ("/", "/", "")
               ]
    )

    bpy.types.Scene.rot_x_nmbr = bpy.props.FloatProperty(
        name="rot_x_nmbr", description="number")
    bpy.types.Scene.rot_y_nmbr = bpy.props.FloatProperty(
        name="rot_y_nmbr", description="number")
    bpy.types.Scene.rot_z_nmbr = bpy.props.FloatProperty(
        name="rot_z_nmbr", description="number")
