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
from . pca_funcs import cleanstr
from .pca_krpfuncs import get_krp_loc, get_krp_align, get_krp_prealign, get_krp_origin
import json


class PCA_OT_panorender(bpy.types.Operator):
    """Render panorama(s) and output the krpano values"""
    bl_idname = "pca.panorender"
    bl_label = "PanoRenderer"

    jsonoutput = []
    pcioutput = []

    multirow = True
    multirow_rotations = [
        (1.5707963705062866, 0.0),
        (1.5707963705062866, 0.7853981852531433),
        (1.5707963705062866, 1.5707963705062866),
        (1.5707963705062866, 2.356194496154785),
        (1.5707963705062866, 3.1415927410125732),
        (1.5707963705062866, 3.9269909858703613),
        (1.5707963705062866, 4.7123894691467285),
        (1.5707963705062866, 5.497787952423096),
        (2.356194496154785, 0.0),
        (2.356194496154785, 1.5707963705062866),
        (2.356194496154785, 3.1415927410125732),
        (2.356194496154785, 4.7123894691467285),
        (0.7853981852531433, 0.0),
        (0.7853981852531433, 1.5707963705062866),
        (0.7853981852531433, 3.1415927410125732),
        (0.7853981852531433, 4.7123894691467285)
    ]

    # output values
    def outputvalues(self, rendercamera, panoname, frame):

        cb_ani = bpy.context.scene.cb_ani
        cb_json = bpy.context.scene.cb_json
        cb_pcijson = bpy.context.scene.cb_pcijson

        decis = bpy.context.scene.panodecis
        renderpano_extension = bpy.context.preferences.addons[
            'panocamadder'].preferences.renderpano_extension

        # rotate rendercam
        # print('Rendercamera rotation: ', rendercamera.rotation_euler[2])
        # rendercamera.rotation_euler[2] -= 1.5708
        # print('Rendercamera rotation: ', rendercamera.rotation_euler[2])
        # rendercamera.rotation_euler[2] += 1.5708
        # print('Rendercamera rotation: ', rendercamera.rotation_euler[2])

        # PCA TXT
        pcatxt = bpy.data.texts['pca.txt']
        if cb_ani == True:
            pcatxt.write(f'Name: {panoname}_{frame}')
        else:
            pcatxt.write(f'Name: {panoname}')

        pcatxt.write('\n')
        pcatxt.write(
            f'origin="{get_krp_origin(rendercamera, decis)[0]}|{get_krp_origin(rendercamera, decis)[1]}|{get_krp_origin(rendercamera, decis)[2]}"\n')
        pcatxt.write(
            f'ox="{get_krp_loc(rendercamera, decis)[0]}" oy="{get_krp_loc(rendercamera, decis)[1]}" oz="{get_krp_loc(rendercamera, decis)[2]}"\n')
        pcatxt.write(
            f'align="{get_krp_align(rendercamera, decis)[0]}|{get_krp_align(rendercamera, decis)[1]}|{get_krp_align(rendercamera, decis)[2]}"\n')
        pcatxt.write(
            f'prealign="{get_krp_prealign(rendercamera, decis)[0]}|{get_krp_prealign(rendercamera, decis)[1]}|{get_krp_prealign(rendercamera, decis)[2]}"\n')
        pcatxt.write('\n')

        # JSON
        if cb_json == True:
            p = {}
            if cb_ani == True:
                p['name'] = f'{panoname}_{frame}'
                p['scene'] = f'scene_{panoname.lower()}_{frame}'
            else:
                p['name'] = f'{panoname}'
                p['scene'] = f'scene_{panoname.lower()}'

            p['origin'] = (get_krp_origin(rendercamera, decis)[0], get_krp_origin(
                rendercamera, decis)[1], get_krp_origin(rendercamera, decis)[2])
            p['location'] = (get_krp_loc(rendercamera, decis)[0], get_krp_loc(
                rendercamera, decis)[1], get_krp_loc(rendercamera, decis)[2])
            p['align'] = (get_krp_align(rendercamera, decis)[0], get_krp_align(
                rendercamera, decis)[1], get_krp_align(rendercamera, decis)[2])
            p['prealign'] = (get_krp_prealign(rendercamera, decis)[0], get_krp_prealign(
                rendercamera, decis)[1], get_krp_prealign(rendercamera, decis)[2])
            self.jsonoutput.append(p)

        # PCI JSON
        if cb_pcijson:
            pci = {}
            if cb_ani == True:
                pci['pano'] = f'{panoname}_{frame}.{renderpano_extension}'
            else:
                pci['pano'] = f'{panoname}.{renderpano_extension}'
            pci['location'] = (round(rendercamera.location[0], decis), round(
                rendercamera.location[1], decis), round(rendercamera.location[2], decis))
            pci['rotation'] = (round(rendercamera.rotation_euler[0], decis), round(
                rendercamera.rotation_euler[1], decis), round(rendercamera.rotation_euler[2], decis))
            self.pcioutput.append(pci)

        return {'FINISHED'}

    # check/add cubecam
    def addRenderCamera(self):
        rendersize = bpy.context.scene.rendersize

        # check/add rendercam
        rendercamera = [cam for cam in bpy.context.scene.objects if cam.type ==
                        'CAMERA' and cam.name == 'PANORENDERCAM']

        if not rendercamera:
            bpy.ops.object.camera_add()
            rendercamera = bpy.context.active_object
            rendercamera.name = 'PANORENDERCAM'
            bpy.context.scene.camera = rendercamera
        else:
            rendercamera = rendercamera[0]
            bpy.context.scene.camera = rendercamera

        bpy.context.view_layer.objects.active = rendercamera

        if bpy.context.scene.render.engine != 'CYCLES':

            bpy.context.object.data.type = 'PERSP'

            if self.multirow == True:
                bpy.context.object.data.lens_unit = 'MILLIMETERS'
                bpy.context.object.data.lens = 15
                bpy.context.scene.render.resolution_y = rendersize
                bpy.context.scene.render.resolution_x = int(rendersize / 3 * 2)
            else:
                bpy.context.object.data.lens_unit = 'FOV'
                bpy.context.object.data.angle = 1.5708
                bpy.context.scene.render.resolution_x = rendersize
                bpy.context.scene.render.resolution_y = rendersize
        else:
            bpy.context.object.data.type = 'PANO'
            try:
                bpy.context.object.data.cycles.panorama_type = 'EQUIRECTANGULAR'  # blender3.6

            except AttributeError:
                bpy.context.object.data.panorama_type = 'EQUIRECTANGULAR'  # blender4.1

            bpy.context.scene.render.resolution_x = rendersize
            bpy.context.scene.render.resolution_y = int(rendersize / 2)

    # render panorama
    def renderpano(self, scenecams, scenecam):

        # checkboxes
        cb_north = bpy.context.scene.cb_north
        cb_ani = bpy.context.scene.cb_ani

        outputpath = bpy.context.scene.render.filepath
        frame = str(bpy.context.scene.frame_current).zfill(4)

        rendercamera = bpy.data.objects['PANORENDERCAM']
        scenecamname = bpy.data.objects[scenecam.name]

        bpy.context.scene.camera = rendercamera

        panoname = cleanstr(bpy.context.scene.pname)

        if len(scenecams) > 1:
            panoname = f'{panoname}_{scenecams.index(scenecamname)}'

        # get scenecam location and rotation
        olmx = scenecam.matrix_world

        lx = olmx.translation[0]
        ly = olmx.translation[1]
        lz = olmx.translation[2]

        rot_euler = scenecam.rotation_euler
        rotmax = scenecam.matrix_world.to_euler('XYZ', rot_euler)
        rx = rotmax[0]
        ry = rotmax[1]
        rz = rotmax[2]

        # set rendercamera location
        rendercamera.location[0] = lx
        rendercamera.location[1] = ly
        rendercamera.location[2] = lz

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = rendercamera
        bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'

        if bpy.context.scene.render.engine != 'CYCLES':

            # multirow
            if self.multirow == True:
                print('Multirow!')
                # print output values
                rendercamera.rotation_euler[0] = self.multirow_rotations[0][0]
                rendercamera.rotation_euler[1] = 0
                rendercamera.rotation_euler[2] = self.multirow_rotations[0][1]
                rendercamera.rotation_euler[0] -= 1.5708
                self.outputvalues(rendercamera, panoname, frame)

                for rot in self.multirow_rotations:
                    print('Rotation:', rot)

                    rendercamera.rotation_euler[0] = rot[0]
                    rendercamera.rotation_euler[1] = 0
                    rendercamera.rotation_euler[2] = rot[1]

                    if cb_ani == True:
                        path = f'{outputpath}{panoname}_{frame}_{str(self.multirow_rotations.index(rot)).zfill(2)}'
                    else:
                        path = f'{outputpath}{panoname}_{str(self.multirow_rotations.index(rot)).zfill(2)}'

                    # render
                    bpy.context.scene.render.filepath = path
                    bpy.ops.render.render(
                        animation=False, write_still=True, use_viewport=False, layer='', scene='')

            # cubafaces
            else:

                # front
                if cb_north == True:
                    rendercamera.rotation_euler[0] = 1.5708
                    rendercamera.rotation_euler[1] = 0
                    rendercamera.rotation_euler[2] = 0
                else:
                    rendercamera.rotation_euler[0] = rx
                    rendercamera.rotation_euler[1] = ry
                    rendercamera.rotation_euler[2] = rz
                if cb_ani == True:
                    path = f'{outputpath}{panoname}_{frame}_f'
                else:
                    path = f'{outputpath}{panoname}_f'

                # print output values
                rendercamera.rotation_euler[0] -= 1.5708
                self.outputvalues(rendercamera, panoname, frame)
                rendercamera.rotation_euler[0] += 1.5708

                # render
                bpy.context.scene.render.filepath = path
                bpy.ops.render.render(
                    animation=False, write_still=True, use_viewport=False, layer='', scene='')

                # left
                if cb_north == True:
                    rendercamera.rotation_euler[2] = 1.5708
                else:
                    scenecam.select_set(False)
                    rendercamera.select_set(True)
                    bpy.ops.transform.rotate(
                        value=-1.5708, orient_axis='Y', orient_type='LOCAL')
                if cb_ani == True:
                    path = f'{outputpath}{panoname}_{frame}_l'
                else:
                    path = f'{outputpath}{panoname}_l'
                bpy.context.scene.render.filepath = path
                bpy.ops.render.render(
                    animation=False, write_still=True, use_viewport=False, layer='', scene='')

                # back
                if cb_north == True:
                    rendercamera.rotation_euler[2] = 3.14159
                else:
                    bpy.ops.transform.rotate(
                        value=-1.5708, orient_axis='Y', orient_type='LOCAL')
                if cb_ani == True:
                    path = f'{outputpath}{panoname}_{frame}_b'
                else:
                    path = f'{outputpath}{panoname}_b'
                bpy.context.scene.render.filepath = path
                bpy.ops.render.render(
                    animation=False, write_still=True, use_viewport=False, layer='', scene='')

                # right
                if cb_north == True:
                    rendercamera.rotation_euler[2] = 4.71239
                else:
                    bpy.ops.transform.rotate(
                        value=-1.5708, orient_axis='Y', orient_type='LOCAL')
                if cb_ani == True:
                    path = f'{outputpath}{panoname}_{frame}_r'
                else:
                    path = f'{outputpath}{panoname}_r'
                bpy.context.scene.render.filepath = path
                bpy.ops.render.render(
                    animation=False, write_still=True, use_viewport=False, layer='', scene='')

                # up
                if cb_north == True:
                    rendercamera.rotation_euler[0] = 3.14159
                    rendercamera.rotation_euler[2] = 0
                else:
                    scenecam.select_set(False)
                    rendercamera.select_set(True)
                    rendercamera.rotation_euler[0] = rx
                    rendercamera.rotation_euler[1] = ry
                    rendercamera.rotation_euler[2] = rz
                    bpy.ops.transform.rotate(
                        value=-1.5708, orient_axis='X', orient_type='LOCAL')

                if cb_ani == True:
                    path = f'{outputpath}{panoname}_{frame}_u'
                else:
                    path = f'{outputpath}{panoname}_u'
                bpy.context.scene.render.filepath = path
                bpy.ops.render.render(
                    animation=False, write_still=True, use_viewport=False, layer='', scene='')

                # down
                if cb_north == True:
                    rendercamera.rotation_euler[0] = 0
                else:
                    rendercamera.rotation_euler[0] = rx
                    rendercamera.rotation_euler[1] = ry
                    rendercamera.rotation_euler[2] = rz
                    bpy.ops.transform.rotate(
                        value=1.5708, orient_axis='X', orient_type='LOCAL')

                if cb_ani == True:
                    path = f'{outputpath}{panoname}_{frame}_d'
                else:
                    path = f'{outputpath}{panoname}_d'
                bpy.context.scene.render.filepath = path
                bpy.ops.render.render(
                    animation=False, write_still=True, use_viewport=False, layer='', scene='')

        # CYCLES equirectangular
        else:
            if cb_north == True:
                rendercamera.rotation_euler[0] = 1.5708
                rendercamera.rotation_euler[1] = 0
                rendercamera.rotation_euler[2] = 0
            else:
                rendercamera.rotation_euler[0] = rx
                rendercamera.rotation_euler[1] = ry
                rendercamera.rotation_euler[2] = rz

            if cb_ani == True:
                path = f'{outputpath}{panoname}_{frame}'
            else:
                path = f'{outputpath}{panoname}'

            # print output values
            rendercamera.rotation_euler[0] -= 1.5708
            self.outputvalues(rendercamera, panoname, frame)
            rendercamera.rotation_euler[0] += 1.5708

            # render
            bpy.context.scene.render.filepath = path
            bpy.ops.render.render(
                animation=False, write_still=True, use_viewport=False, layer='', scene='')

        # reset outputpath
        bpy.context.scene.render.filepath = outputpath

        return {'FINISHED'}

    # MAIN
    def execute(self, context):

        # todo: check if outputpath exists
        # outputpath = bpy.context.scene.render.filepath
        # print(f'Outputpath: {outputpath}')

        # check if fileformat is set to image
        filef = bpy.context.scene.render.image_settings.file_format
        if filef == 'AVI_JPEG' or filef == 'AVI_RAW' or filef == 'FFMPEG':
            self.report(
                {'WARNING'}, 'No render. Choose an image format as output!')
        else:
            cb_ani = bpy.context.scene.cb_ani
            rendercam = bpy.context.scene.camera
            localcam = bpy.context.space_data.camera

            cb_json = context.scene.cb_json
            cb_pcijson = context.scene.cb_pcijson

            self.jsonoutput = []
            self.pcioutput = []

            # get all cams in selection
            scenecams = [cam for cam in bpy.context.selected_objects if cam.type ==
                         'CAMERA' and cam.name != 'PANORENDERCAM']

            if len(scenecams) == 0:
                self.report({'WARNING'}, 'No camera selected..')
                return {'CANCELLED'}
            else:

                # CREATE JSON/TXT FILES
                # PCA JSON
                if cb_json == True:
                    jsonname = 'pca.JSON'
                    if not jsonname in bpy.data.texts:
                        jsonfile = bpy.data.texts.new(jsonname)
                    else:
                        jsonfile = bpy.data.texts[jsonname]

                # PCI JSON
                if cb_pcijson == True:
                    pcijsonname = 'pci.JSON'
                    if not pcijsonname in bpy.data.texts:
                        pcijsonfile = bpy.data.texts.new(pcijsonname)
                    else:
                        pcijsonfile = bpy.data.texts[pcijsonname]

                # pca txt-file
                txtname = 'pca.txt'
                if not txtname in bpy.data.texts:
                    pcatxt = bpy.data.texts.new(txtname)
                else:
                    pcatxt = bpy.data.texts[txtname]
                    pcatxt.clear()

                bpy.context.scene.camera = None
                bpy.context.space_data.camera = None

                # add render camera if not exists
                self.addRenderCamera()

                # L O O P
                for scenecam in scenecams:

                    if cb_ani == True:
                        startframe = bpy.context.scene.frame_start
                        endframe = bpy.context.scene.frame_end
                        framerange = endframe - startframe + 1

                        bpy.ops.screen.frame_jump(end=False)

                        for f in range(framerange):
                            self.renderpano(scenecams, scenecam)
                            bpy.ops.screen.frame_offset(delta=1)

                    else:
                        self.renderpano(scenecams, scenecam)

                bpy.context.scene.camera = rendercam
                bpy.context.space_data.camera = localcam

                if cb_json:
                    pcajson = json.dumps(self.jsonoutput, indent=4)
                    jsonfile.clear()
                    jsonfile.write(pcajson)
                if cb_pcijson:
                    pcijson = json.dumps(self.pcioutput, indent=4)
                    pcijsonfile.clear()
                    pcijsonfile.write(pcijson)

        return {'FINISHED'}

    # popup dialog
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    # popup message
    def draw(self, context):
        # check fileformat
        filef = bpy.context.scene.render.image_settings.file_format
        if filef == 'AVI_JPEG' or filef == 'AVI_RAW' or filef == 'FFMPEG':
            # popuplayout
            layout = self.layout
            col = layout.column(align=True)
            col.label(text='', icon='ERROR')
            col.label(text='No render. Choose an image format as output!')
        else:
            cb_ani = bpy.context.scene.cb_ani

            scenecams = [cam for cam in bpy.context.selected_objects if cam.type ==
                         'CAMERA' and cam.name != 'PANORENDERCAM']
            scenecamslen = len(scenecams)

            if scenecamslen >= 1:
                # frames
                if cb_ani == True:
                    startframe = bpy.context.scene.frame_start
                    endframe = bpy.context.scene.frame_end
                    framerange = endframe - startframe + 1
                else:
                    framerange = 1
                framesinfo = f'Frames: {framerange}'
                pcaminfo = f'Cameras: {scenecamslen}'

                # cubefacecount
                if bpy.context.scene.render.engine != 'CYCLES':
                    if self.multirow == True:
                        cubefacecount = framerange * len(
                            self.multirow_rotations) * scenecamslen
                        renderinfo = f'{cubefacecount} multirow images will be rendered!'
                    else:
                        cubefacecount = framerange * 6 * scenecamslen
                        renderinfo = f'{cubefacecount} cubeface images will be rendered!'
                else:
                    equicount = framerange * scenecamslen
                    renderinfo = f'{equicount} equirectangular panorama will be rendered!'

                # popuplayout
                layout = self.layout

                col = layout.column(align=True)
                col.label(text='', icon='INFO')
                col.label(text=f'{pcaminfo}; {framesinfo}')
                col.label(text=renderinfo)

                box = layout.box()
                col = box.column(align=True)
                col.label(text='WARNING', icon='ERROR')
                col.label(
                    text='* The rendertime depends on your render settings!')
                col.label(text='* This window is closed when the')
                col.label(text='   rendering process is complete.')
            else:
                layout = self.layout
                col = layout.column(align=True)
                col.label(text='', icon='INFO')
                col.label(text='No camera selected..')
