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
from bpy_extras.io_utils import ImportHelper
import os
import json


def validPCiJSON(pcijsonpano):
    pano_valid = False
    loc_valid = False
    rot_valid = False

    if 'pano' in pcijsonpano:
        if type(pcijsonpano['pano']) == str:
            pano_valid = True

    if 'location' in pcijsonpano:
        location = pcijsonpano['location']
        if type(location) == list:
            if len(location) == 3:
                if type(location[0]) == int or type(location[0]) == float:
                    if type(location[1]) == int or type(location[1]) == float:
                        if type(location[2]) == int or type(location[2]) == float:
                            loc_valid = True

    if 'rotation' in pcijsonpano:
        rotation = pcijsonpano['rotation']
        if type(rotation) == list:
            if len(rotation) == 3:
                if type(rotation[0]) == int or type(rotation[0]) == float:
                    if type(rotation[1]) == int or type(rotation[1]) == float:
                        if type(rotation[2]) == int or type(rotation[2]) == float:
                            rot_valid = True

    if pano_valid and loc_valid and rot_valid:
        return True


def update_panonmbr_max():
    max_panonmbr = len(bpy.types.Scene.pcijson)
    if max_panonmbr < 1:
        max_panonmbr = 1
    bpy.types.Scene.panonmbr = bpy.props.IntProperty(
        name="panonmbr",
        description="panonmbr",
        min=1,
        max=max_panonmbr
    )


class PCA_OT_loadpcijson(bpy.types.Operator, ImportHelper):
    """Open the file dialog box"""
    bl_label = "Load PCI JSON"
    bl_idname = "pca.loadpcijson"
    bl_options = {'UNDO'}

    filter_glob: bpy.props.StringProperty(
        default='*.json;*.JSON;',
        options={'HIDDEN'}
    )  # type: ignore

    def execute(self, context):
        """  """

        filename, extension = os.path.splitext(self.filepath)
        jsonfilename = os.path.splitext(
            os.path.basename(f'{filename}{extension}'))[0]

        bpy.types.Scene.jsonpath = os.path.dirname(self.filepath)

        try:
            with open(self.filepath, 'r') as json_file:
                data = json.load(json_file)
                bpy.types.Scene.jsonfile = f"{jsonfilename}{extension}"
                bpy.types.Scene.jsondata = data

                bpy.types.Scene.pcijson.clear()

                for item in bpy.types.Scene.jsondata:
                    if validPCiJSON(item) == True:
                        bpy.types.Scene.pcijson.append(item)

                context.scene.panonmbr = 0
                update_panonmbr_max()

        except ValueError as err:
            bpy.types.Scene.jsonfile = f"{jsonfilename}{extension} (INVALIDE)"
            print(f'INVALIDE JSON {err}')

        return {'FINISHED'}
