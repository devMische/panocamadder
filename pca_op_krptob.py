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
from math import radians
import mathutils


class PCAPLUS_OT_torxryrz(bpy.types.Operator):
    """Rotate the object to rx ry rz"""
    bl_idname = "pcaplus.torxryrz"
    bl_label = "Move to krp position"
    bl_options = {'UNDO'}

    def execute(self, context):

        inp = context.scene.krpcode

        obj = bpy.context.active_object
        krpvals = 0

        if obj != None:
            try:
                if 'rx="' in inp:
                    rxs = inp.index('rx="') + 4
                    rxe = inp.index('"', rxs)
                    rx = inp[rxs:rxe]
                    krpvals += 1

                if 'ry="' in inp:
                    rys = inp.index('ry="') + 4
                    rye = inp.index('"', rys)
                    ry = inp[rys:rye]
                    krpvals += 1

                if 'rz="' in inp:
                    rzs = inp.index('rz="') + 4
                    rze = inp.index('"', rzs)
                    rz = inp[rzs:rze]
                    krpvals += 1

            except ValueError:
                krpvals = 0
                self.report(
                    {'WARNING'}, 'Something went wrong.. Please check your input')

            if krpvals == 3:
                obj.rotation_euler[0] = 1 * radians(float(rx) + 90)
                obj.rotation_euler[1] = 1 * radians(float(rz))
                obj.rotation_euler[2] = -1 * radians(float(ry))
                krpvals = 0

        else:
            krpvals = 0
            self.report(
                {'WARNING'}, 'Something went wrong.. No active object found')

        return {'FINISHED'}


class PCAPLUS_OT_toprealign(bpy.types.Operator):
    """Rotate the object to (pre)align position"""
    bl_idname = "pcaplus.toprealign"
    bl_label = "Rotate to (pre)align"
    bl_options = {'UNDO'}

    def execute(self, context):

        inp = context.scene.krpcode

        obj = bpy.context.active_object
        krpvals = 0

        if obj != None:

            try:
                ispre = False
                if 'prealign="' in inp:

                    ispre = True

                    pxs = inp.index('prealign="') + 10
                    pxe = inp.index('|', pxs)
                    px = inp[pxs:pxe]
                    krpvals += 1

                    pys = pxe + 1
                    pye = inp.index('|', pys)
                    py = inp[pys:pye]
                    krpvals += 1

                    pzs = pye + 1
                    pze = inp.index('"', pzs)
                    pz = inp[pzs:pze]
                    krpvals += 1

                if 'align="' in inp and ispre == False:

                    pxs = inp.index('align="') + 7
                    pxe = inp.index('|', pxs)
                    px = inp[pxs:pxe]
                    krpvals += 1

                    pys = pxe + 1
                    pye = inp.index('|', pys)
                    py = inp[pys:pye]
                    krpvals += 1

                    pzs = pye + 1
                    pze = inp.index('"', pzs)
                    pz = inp[pzs:pze]
                    krpvals += 1

            except ValueError:
                krpvals = 0
                self.report(
                    {'WARNING'}, 'Something went wrong.. Please check your input')

            # to prealign
            if krpvals == 3 and ispre == True:
                obj.rotation_euler[0] = -1 * radians(float(px))
                obj.rotation_euler[1] = -1 * radians(float(pz))
                obj.rotation_euler[2] = -1 * radians(float(py))
                krpvals = 0
            # to align
            if krpvals == 3 and ispre == False:

                x = radians(float(px))
                y = radians(float(py))
                z = radians(float(pz))

                rotALIGN = mathutils.Euler((z, x, y), 'YXZ')
                rotMAT = rotALIGN.to_matrix()
                rotXYZ = rotMAT.to_euler('XYZ')

                obj.rotation_mode = 'YXZ'
                obj.rotation_euler = rotXYZ
                obj.rotation_mode = 'XYZ'

                krpvals = 0

        else:
            krpvals = 0
            self.report(
                {'WARNING'}, 'Something went wrong.. No active object found')

        return {'FINISHED'}


class PCAPLUS_OT_tooxoyoz(bpy.types.Operator):
    """Move the object to ox/oy/oz ox/oy/oz"""
    bl_idname = "pcaplus.tooxoyoz"
    bl_label = "Move to krp position"
    bl_options = {'UNDO'}

    def execute(self, context):

        inp = context.scene.krpcode

        obj = bpy.context.active_object
        krpvals = 0

        if obj != None:

            try:
                if 'ox="' in inp:
                    oxs = inp.index('ox="') + 4
                    oxe = inp.index('"', oxs)
                    ox = inp[oxs:oxe]
                    krpvals += 1

                if 'oy="' in inp:
                    oys = inp.index('oy="') + 4
                    oye = inp.index('"', oys)
                    oy = inp[oys:oye]
                    krpvals += 1

                if 'oz="' in inp:
                    ozs = inp.index('oz="') + 4
                    oze = inp.index('"', ozs)
                    oz = inp[ozs:oze]
                    krpvals += 1

                if 'tx="' in inp:
                    oxs = inp.index('tx="') + 4
                    oxe = inp.index('"', oxs)
                    ox = inp[oxs:oxe]
                    krpvals += 1

                if 'ty="' in inp:
                    oys = inp.index('ty="') + 4
                    oye = inp.index('"', oys)
                    oy = inp[oys:oye]
                    krpvals += 1

                if 'tz="' in inp:
                    ozs = inp.index('tz="') + 4
                    oze = inp.index('"', ozs)
                    oz = inp[ozs:oze]
                    krpvals += 1
            except ValueError:
                krpvals = 0
                self.report(
                    {'WARNING'}, 'Something went wrong.. Please check your input')

            if krpvals == 3:
                obj.location[0] = float(ox) / 100
                obj.location[1] = float(oz) / 100
                obj.location[2] = float(oy) / -100

                krpvals = 0

        else:
            krpvals = 0
            self.report(
                {'WARNING'}, 'Something went wrong.. No active object found')

        return {'FINISHED'}


class PCAPLUS_OT_todcenter(bpy.types.Operator):
    """Move object to depthmap.center"""
    bl_idname = "pcaplus.todcenter"
    bl_label = "Move to krp origin"
    bl_options = {'UNDO'}

    def execute(self, context):

        inp = context.scene.krpcode

        obj = bpy.context.active_object
        krpvals = 0
        oc = 'oc'

        if obj != None:

            try:
                # center
                if 'center="' in inp:
                    oc = 'c'
                    pxs = inp.index('center="') + 8
                    pxe = inp.index(',', pxs)
                    px = inp[pxs:pxe]
                    krpvals += 1

                    pys = pxe + 1
                    pye = inp.index(',', pys)
                    py = inp[pys:pye]
                    krpvals += 1

                    pzs = pye + 1
                    pze = inp.index('"', pzs)
                    pz = inp[pzs:pze]
                    krpvals += 1

                # origin
                if 'origin="' in inp:
                    oc = 'o'
                    pxs = inp.index('origin="') + 8
                    pxe = inp.index(',', pxs)
                    px = inp[pxs:pxe]
                    krpvals += 1

                    pys = pxe + 1
                    pye = inp.index(',', pys)
                    py = inp[pys:pye]
                    krpvals += 1

                    pzs = pye + 1
                    pze = inp.index('"', pzs)
                    pz = inp[pzs:pze]
                    krpvals += 1

            except ValueError:
                krpvals = 0
                self.report(
                    {'WARNING'}, 'Something went wrong.. Please check your input')

            if krpvals == 3:
                # center
                if oc == 'c':
                    obj.location[0] = float(pz) * -1
                    obj.location[1] = float(px)
                    obj.location[2] = float(py)
                # origin
                if oc == 'o':
                    obj.location[0] = float(px) * -1
                    obj.location[1] = float(pz) * -1
                    obj.location[2] = float(py)

                krpvals = 0

        else:
            krpvals = 0
            self.report(
                {'WARNING'}, 'Something went wrong.. No active object found')

        return {'FINISHED'}
