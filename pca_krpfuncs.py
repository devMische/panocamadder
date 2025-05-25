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
from math import degrees
import mathutils
from mathutils import Vector

# SCALE


def get_krp_scale(obj, decs):
    if round(obj.scale[0], 2) == round(obj.scale[1], 2) and round(obj.scale[0], 2) == round(obj.scale[2], 2) and round(obj.scale[1], 2) == round(obj.scale[2], 2):
        sc = round((obj.scale[0] + obj.scale[1] + obj.scale[2]) / 3, decs)

    else:
        sc = 'non conform scaling'

    return sc

# SCALE3D


def get_krp_scale_3d(obj, decs):

    olmx = obj.matrix_world

    sx = round(olmx.to_scale()[0], decs)
    sy = round(olmx.to_scale()[2], decs)
    sz = round(olmx.to_scale()[1], decs)

    return sx, sy, sz


# LOCATION
def get_krp_loc(obj, decs):
    olmx = obj.matrix_world
    lx = olmx.translation[0]
    ly = olmx.translation[1]
    lz = olmx.translation[2]

    klx = round(lx * 100, decs)
    kly = round(lz * -100, decs)
    klz = round(ly * 100, decs)

    return klx, kly, klz


# ORIGIN
def get_krp_origin(obj, decs):
    olmx = obj.matrix_world
    x = round(olmx.translation[0], decs)
    y = round(olmx.translation[2], decs) * -1
    z = round(olmx.translation[1], decs)

    return x, y, z


# CENTER
def get_krp_center(obj, decs):
    olmx = obj.matrix_world
    x = round(olmx.translation[1], decs)
    y = round(olmx.translation[2], decs)
    z = round(olmx.translation[0] * -1, decs)

    return x, y, z


# ROTATION (txt/img Hotspot)
def get_krp_rot(obj, decs):
    rot_euler = obj.rotation_euler
    rotmax = obj.matrix_world.to_euler('XYZ', rot_euler)

    hsrx = round(degrees(rotmax[0]) - 90, decs)
    hsry = round(degrees(rotmax[2]) * -1, decs)
    hsrz = round(degrees(rotmax[1]), decs)

    return hsrx, hsry, hsrz


# ROTATION (3D Hotspot)
def get_krp_rot_3d(obj, decs):
    rot_euler = obj.rotation_euler
    rotmax = obj.matrix_world.to_euler('XYZ', rot_euler)

    hsrx = round(degrees(rotmax[0]), decs)
    hsry = round(degrees(rotmax[2]) * -1, decs)
    hsrz = round(degrees(rotmax[1]), decs)

    return hsrx, hsry, hsrz


# PREALIGN
def get_krp_prealign(obj, decs):
    rot_euler = obj.rotation_euler
    rotmax = obj.matrix_world.to_euler('XYZ', rot_euler)

    x = round(-1 * degrees(rotmax[0]), decs)
    y = round(-1 * degrees(rotmax[2]), decs)
    z = round(-1 * degrees(rotmax[1]), decs)

    return x, y, z


# ALIGN
def get_krp_align(obj, decs):

    rot_euler = obj.rotation_euler
    rotmax = obj.matrix_world.to_euler('YXZ', rot_euler)

    x = round(degrees(rotmax[1]), decs)
    y = round(degrees(rotmax[2]), decs)
    z = round(degrees(rotmax[0]), decs)

    return x, y, z


# WIDTH HEIGHT
def get_krp_wh(obj):
    s = get_krp_scale(obj, 8)
    try:
        w = round(obj.dimensions[0] * 50 / s)
        h = round(obj.dimensions[1] * 50 / s)

    except TypeError:
        w = 'non conform scaling'
        h = 'non conform scaling'

    return w, h


# HLOOKAT VLOOKAT
def get_krp_lookat(obj, decs):
    rot_euler = obj.rotation_euler
    rotmax = obj.matrix_world.to_euler('XYZ', rot_euler)
    rotmaxl = obj.matrix_local.to_euler('XYZ', rot_euler)

    hl = degrees(rotmax[2]) * -1
    vl = -1 * degrees(rotmaxl[0]) + 90

    # 180 math hlookat
    while hl > 180 or hl < -180:
        if hl > 180:
            hl = hl - 360
        if hl < -180:
            hl = hl + 360

    return round(hl, decs), round(vl, decs)


# EULER TO DIRECTION VECTOR
def euler_to_direction_vector(rot_x, rot_y, rot_z):

    # Initialen Vektor definieren (hier entlang der negativen Z-Achse, da Sonnenlicht typischerweise nach unten zeigt)
    direction = Vector((0.0, 0.0, -1.0))

    # Rotationsmatrix basierend auf den Euler-Winkeln erstellen
    euler_rotation = mathutils.Euler((rot_x, rot_y, rot_z), 'XYZ')

    # Rotationsmatrix auf den Vektor anwenden
    rotated_direction = euler_rotation.to_matrix() @ direction

    return rotated_direction


# SUN POSITION
def get_krp_sunpos(obj, decs):

    global_rotation_euler = obj.matrix_world.to_euler()
    global_rot_x = math.degrees(global_rotation_euler.x)
    global_rot_y = math.degrees(global_rotation_euler.y)
    global_rot_z = math.degrees(global_rotation_euler.z)

    rot_x_rad = math.radians(global_rot_x)
    rot_y_rad = math.radians(global_rot_y)
    rot_z_rad = math.radians(global_rot_z)

    vec = euler_to_direction_vector(rot_x_rad, rot_y_rad, rot_z_rad)

    azimutal_winkel = math.degrees(math.atan2(vec.y, vec.x))

    polar_winkel = math.degrees(math.acos(vec.z / vec.length))

    atv = 90 - polar_winkel

    ath = 270 - azimutal_winkel
    if ath < 0:
        ath += 360
    if ath > 360:
        ath -= 360

    return round(ath, 2), round(atv, 2)


# FOV
def get_krp_fov(obj, decs):
    if obj.type == 'CAMERA':
        cam = bpy.context.object.data.name
        fov = round(degrees(bpy.data.cameras[cam].angle), decs)

    return fov


def rotate_vector(vector, rotation):
    """ 
    Rotiert einen Vektor um Euler-Winkel (XYZ-Reihenfolge).

    Parameter:
    - vector: Ein Vektor (x, y, z) als Tuple.
    - rotation: Rotation als Tuple (rot_x, rot_y, rot_z) in Radianten.

    Rückgabe:
    - Der rotierte Vektor (x', y', z').
    """
    x, y, z = vector
    rot_x, rot_y, rot_z = rotation

    cos_x = math.cos(rot_x)
    sin_x = math.sin(rot_x)
    y, z = cos_x * y - sin_x * z, sin_x * y + cos_x * z

    cos_y = math.cos(rot_y)
    sin_y = math.sin(rot_y)
    x, z = cos_y * x + sin_y * z, -sin_y * x + cos_y * z

    cos_z = math.cos(rot_z)
    sin_z = math.sin(rot_z)
    x, y = cos_z * x - sin_z * y, sin_z * x + cos_z * y

    return (x, y, z)


def get_krp_spottarget(spotlamp):  # location, rotation, length

    x0, y0, z0 = spotlamp.matrix_world.translation

    # matrix rotation
    rot_euler = spotlamp.rotation_euler
    # rotmax = spotlamp.matrix_world.to_euler('XYZ', rot_euler)
    rotmaxlocal = spotlamp.matrix_local.to_euler('XYZ', rot_euler)

    # Startvektor des Strahls (negativ entlang der Z-Achse, da das Licht nach unten gerichtet ist)
    direction = (0.0, 0.0, -1.0)

    # Rotierte Richtung basierend auf den Euler-Winkeln
    rotated_direction = rotate_vector(direction, rotmaxlocal)

    # Berechne den Endpunkt
    x1 = x0 + rotated_direction[0] * spotlamp.data.cutoff_distance
    y1 = y0 + rotated_direction[1] * spotlamp.data.cutoff_distance
    z1 = z0 + rotated_direction[2] * spotlamp.data.cutoff_distance

    klx = x1 * 100
    kly = z1 * -100
    klz = y1 * 100

    return (klx, kly, klz)
