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
import math
import bmesh


def replace_last(source_string, replace_what, replace_with):
    if source_string.endswith(replace_what):
        return source_string[:-len(replace_what)] + replace_with
    return source_string

# cleanstring


def cleanstr(s):
    s = s.strip()
    s = s.replace('ä', 'ae')
    s = s.replace('ö', 'oe')
    s = s.replace('ü', 'ue')
    s = s.replace('Ä', 'Ae')
    s = s.replace('Ö', 'Oe')
    s = s.replace('Ü', 'Ue')
    s = s.replace('ß', 'ss')
    s = s.replace(' ', '_')

    return s


def remove_pca_naming(s):
    s = replace_last(s, '_HANDLE', '')
    s = replace_last(s, '_EMPTY', '')
    s = replace_last(s, '_CAM', '')
    s = replace_last(s, '_DEPTH', '')
    s = replace_last(s, '_TOUR', '')
    return s


def check_if_hs_color(obj):
    for s in obj.material_slots:
        if s.material and s.material.use_nodes:
            for rgbn in s.material.node_tree.nodes:
                if rgbn.name == 'pca-hscolor':
                    return True
    return False


def check_if_hs_alpha(obj):
    for s in obj.material_slots:
        if s.material and s.material.use_nodes:
            for n in s.material.node_tree.nodes:
                if n.name == 'pca-hsalpha-mixer':
                    return True
    return False


# imgtex
def get_pca_img_texture(obj):
    imgname = ''
    for s in obj.material_slots:
        if s.material and s.material.use_nodes:
            for n in s.material.node_tree.nodes:
                if n.label == 'PCAIMGTEX':
                    imgname = n.image.name
                    if imgname[len(imgname) - 1].isdigit():
                        imgname = imgname[:-4]
    return imgname


def lin_to_srgb(c):
    if c < 0.0031308:
        srgb = 0.0 if c < 0.0 else c * 12.92
    else:
        srgb = 1.055 * math.pow(c, 1.0 / 2.4) - 0.055
    return max(min(int(srgb * 255 + 0.5), 255), 0)


def hextriplet(c):
    return '0x' + ''.join(f'{i:02X}' for i in c)


def floats_to_hex(f_r, f_g, f_b):

    srgb = [lin_to_srgb(c) for c in (f_r, f_g, f_b)]
    hex = hextriplet(srgb)

    return hex

# bgcolor


def get_pca_color(obj):
    hexcol = ''
    for s in obj.material_slots:
        if s.material and s.material.use_nodes:
            for n in s.material.node_tree.nodes:
                if n.name == 'pca-hscolor':
                    bgclr = n.outputs[0].default_value

                    hexcol = floats_to_hex(bgclr[0], bgclr[1], bgclr[2])

    return hexcol


# alpha
def get_pca_alpha(obj, decs):
    hsalpha = 1.0
    for s in obj.material_slots:
        if s.material and s.material.use_nodes:
            for n in s.material.node_tree.nodes:
                if n.name == 'pca-hsalpha-mixer':
                    hsalpha = round(n.inputs[0].default_value, decs)

    return hsalpha


def check_if_faces(obj):
    flist = []
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    for f in bm.faces:
        if f.select:
            flist.append(f)

    if len(flist) == 0:
        return False
    else:
        return True


def get_pano_path(material):

    mat = bpy.data.materials[material]

    # check if the material exists
    if not mat:
        return None

    # check if the material uses nodes
    if not mat.use_nodes:
        return None

    def search_node_tree(tree):

        depth_texture_path = None
        for node in tree.nodes:
            if node.name == "Environment Texture":
                depth_texture_path = node.image.filepath
                return str(depth_texture_path)

            if node.type == 'GROUP' and node.node_tree is not None:
                search_node_tree(node.node_tree)
                found = search_node_tree(node.node_tree)
                if found:
                    return found

        return None

    node_tree = mat.node_tree
    path = search_node_tree(node_tree)

    return path
