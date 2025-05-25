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
import bmesh
from math import dist
from . pca_funcs import cleanstr, check_if_faces


# dollhousetexture
class PCAPLUS_OT_dollhousetexture(bpy.types.Operator):
    """Create dollhouse texture"""
    bl_idname = "pcaplus.dollhousetexture"
    bl_label = "distribute pano materials"
    bl_options = {'UNDO'}

    def execute(self, context):

        # clean / prepare model
        def cleanModel(obj):

            selected = []
            for item in bpy.context.selected_objects:
                selected.append(item)
                item.select_set(False)

            obj.select_set(True)  # Select the object
            context.view_layer.objects.active = obj  # Set the object as the active object

            # apply transforms
            bpy.ops.object.transform_apply(
                location=True, rotation=True, scale=True)

            for item in selected:
                item.select_set(True)
            obj.select_set(True)  # Select the object
            context.view_layer.objects.active = obj  # Set the object as the active object

            for i in range(len(obj.material_slots)):
                obj.active_material_index = 0
                bpy.ops.object.material_slot_remove()

            # remove doubles
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()
            bpy.ops.mesh.select_all(action='DESELECT')

            # objectmode
            bpy.ops.object.mode_set(mode='OBJECT')

        def getAngleRef(point, direction):
            x = (point[0]) + direction[0]
            y = (point[1]) + direction[1]
            z = (point[2]) + direction[2]

            return (x, y, z)

        def returnDirection(direction):
            x = direction[0] * -1
            y = direction[1] * -1
            z = direction[2] * -1

            return (x, y, z)

        # Create list with dictonaries for each polygon

        def makePlygonDict():
            for face in fcs:

                p = {'face': face.index,
                     'location': (0.0, 0.0, 0.0),
                     'faceangleref': (0.0, 0.0, 0.0),
                     'anglerefdistance': float('inf'),
                     'matdistance': float('inf'),
                     'material': 'no_MAT'}
                polys.append(p)

        # update polygon-dictionatries (location and normal)

        def getFaceInfo():

            # get current mesh
            current_mesh = obj.data

            # create empty bmesh, add current mesh into empty bmesh
            current_bm = bmesh.new()
            current_bm.from_mesh(current_mesh)

            for face in current_bm.faces:

                face_location = obj.matrix_world @ face.calc_center_median()

                polys[face.index].update({'location': face_location})

                fRef = getAngleRef(face_location, face.normal)
                polys[face.index].update({'faceangleref': fRef})

            # current_bmesh back to mesh
            current_bm.to_mesh(current_mesh)
            current_bm.free()

        # raycast from the _HANDLES to each polygon / update polygon-dictionaries

        def matDistribute():

            # check selection
            if len(bpy.context.selected_objects) > 1 and bpy.context.active_object.type == 'MESH':
                dollhouse = bpy.context.active_object

                # loop over _HANDLES
                for item in bpy.context.selected_objects:

                    if item.type == 'EMPTY' and '_HANDLE' in item.name or item.type == 'EMPTY' and '_EMPTY' in item.name:

                        # create materialname
                        material = item.name
                        if '_HANDLE' in material:
                            material = material.replace('_HANDLE', '')
                        if '_EMPTY' in material:
                            material = material.replace('_EMPTY', '')
                        material = material + '_MAT'

                        ray_begin = item.location

                        for p in polys:

                            ray_end = p.get('location')
                            ray_direction = ray_end - ray_begin
                            ray_direction.normalize()

                            # covert ray_begin to "dollhouse" local space
                            ray_begin_local = dollhouse.matrix_world.inverted() @ ray_begin
                            ray_end_local = dollhouse.matrix_world.inverted() @ ray_end

                            # do ray cast on dollhouse
                            cast_result = dollhouse.ray_cast(
                                ray_begin_local, ray_direction)

                            # update polys
                            if cast_result[0] == True and dist(ray_end_local, cast_result[1]) < 0.1:

                                distance = dist(
                                    item.location, p.get("location"))
                                newangleref = getAngleRef(
                                    p.get("location"), returnDirection(ray_direction))
                                newanglerefdistance = dist(
                                    newangleref, p.get("faceangleref"))

                                # distance-based
                                if anglebased == False:

                                    if distance < p.get("matdistance") and newanglerefdistance < 1.41:

                                        polys[cast_result[3]].update(
                                            {'matdistance': distance})
                                        polys[cast_result[3]].update(
                                            {'material': material})
                                        polys[cast_result[3]].update(
                                            {'anglerefdistance': newanglerefdistance})

                                # angle-based
                                else:
                                    if distance < maxdistance:

                                        if newanglerefdistance < p.get("anglerefdistance"):
                                            polys[cast_result[3]].update(
                                                {'matdistance': distance})
                                            polys[cast_result[3]].update(
                                                {'material': material})
                                            polys[cast_result[3]].update(
                                                {'anglerefdistance': newanglerefdistance})
                                    else:
                                        # same as anglebased == False
                                        if distance < p.get("matdistance"):
                                            polys[cast_result[3]].update(
                                                {'matdistance': distance})
                                            polys[cast_result[3]].update(
                                                {'material': material})
                                            polys[cast_result[3]].update(
                                                {'anglerefdistance': newanglerefdistance})

        # create no_MAT

        def createNoMat(matname):
            # pref colors
            nomatcolor = bpy.context.preferences.addons['panocamadder'].preferences.nomatcolor
            xmatcolor = bpy.context.preferences.addons['panocamadder'].preferences.xmatcolor

            # creat new
            nomat = bpy.data.materials.new(name=matname)
            nomat.use_nodes = True

            # Remove default material
            nomat.node_tree.nodes.remove(
                nomat.node_tree.nodes.get('Principled BSDF'))
            nomat_output = nomat.node_tree.nodes.get('Material Output')

            # add emission
            noemi_node = nomat.node_tree.nodes.new('ShaderNodeEmission')
            nomat.node_tree.nodes["Emission"]
            if nomat.name == "no_MAT":
                noemi_node.inputs[0].default_value = nomatcolor
            else:
                noemi_node.inputs[0].default_value = xmatcolor
            noemi_node.location = (-30, 200)

            #  link shaders
            nomat.node_tree.links.new(
                noemi_node.outputs[0], nomat_output.inputs[0])
            nomat.use_backface_culling = True

        # sort polygonlist to matlist

        def fillMats():

            m = {}

            for p in polys:

                ma = p.get('material')
                fa = p.get('face')

                # first item
                if len(mats) == 0:
                    m = {'mat': ma,
                         'faces': [fa]}
                    mats.append(m)

                else:

                    for m in mats:
                        if ma == m.get('mat'):

                            m.get('faces').append(fa)
                            break
                    else:

                        mnew = {'mat': ma,
                                'faces': [fa]}

                        mats.append(mnew)

        # APPLY PanoMATs

        def applyPanoMats():

            dollhouse = bpy.context.active_object

            # check/create no_MAT
            nomat = bpy.data.materials.get("no_MAT")
            if not nomat:
                createNoMat("no_MAT")

            # add no_MAT
            bpy.ops.object.material_slot_add()
            dollhouse.material_slots[0].material = bpy.data.materials['no_MAT']

            # assign to ALL faces
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.material_slot_assign()
            bpy.ops.object.mode_set(mode='OBJECT')

            if len(mats) >= 1:
                mx = 0
                for m in mats:

                    if m.get('mat') != 'no_MAT':
                        mx += 1
                        mat = m.get('mat')
                        facelist = m.get('faces')

                        # create _NOT-FOUND material if needed
                        if mat not in bpy.data.materials:
                            mat = 'X_' + mat
                            if mat not in bpy.data.materials:
                                createNoMat(mat)

                        # add new mat to slot
                        dollhouse.data.materials.append(
                            bpy.data.materials[mat])

                        # editmode
                        bpy.ops.object.mode_set(mode='EDIT')
                        # deselect all
                        bpy.ops.mesh.select_all(action='DESELECT')
                        # objectmode
                        bpy.ops.object.mode_set(mode='OBJECT')

                        # assign material to faces
                        for f in facelist:
                            dollhouse.data.polygons[f].material_index = mx

                # remove unused materials
                bpy.ops.object.material_slot_remove_unused()

        # RUN
        goodselection = False

        if len(bpy.context.selected_objects) > 1 and bpy.context.active_object.type == 'MESH':

            for item in bpy.context.selected_objects:

                if item.type == 'EMPTY' and '_HANDLE' in item.name or item.type == 'EMPTY' and '_EMPTY' in item.name:
                    goodselection = True
                    # break

            if goodselection:

                # checkbox
                cb_anglebased = context.scene.cb_anglebased
                cb_protectfacemask = context.scene.cb_protectfacemask
                maxdistance = context.scene.anglemaxdist[0]

                if cb_anglebased:
                    anglebased = True
                else:
                    anglebased = False

                obj = bpy.context.active_object
                fcs = obj.data.polygons
                polys = []
                mats = []

                if cb_protectfacemask and len(obj.vertex_groups) > 0:

                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='DESELECT')

                    # select vertex group, switch to edge and face mode
                    bpy.ops.object.vertex_group_select()
                    bpy.ops.mesh.select_mode(
                        use_extend=False, use_expand=False, type='EDGE')
                    bpy.ops.mesh.select_mode(
                        use_extend=False, use_expand=False, type='FACE')

                    hasFaces = False
                    if check_if_faces(obj) == True:
                        hasFaces = True

                        bpy.ops.mesh.separate(type='SELECTED')
                        bpy.ops.object.mode_set(mode='OBJECT')
                        bpy.context.active_object.select_set(False)
                        # get objectcopy
                        for splitobj in bpy.context.selected_objects:
                            bpy.context.view_layer.objects.active = splitobj
                        bpy.context.active_object.select_set(False)
                        obj.select_set(True)  # Select the object
                        context.view_layer.objects.active = obj
                    else:
                        self.report(
                            {'WARNING'}, "Vertexgroup contains no faces")
                        bpy.ops.object.mode_set(mode='OBJECT')

                cleanModel(obj)
                makePlygonDict()
                getFaceInfo()
                matDistribute()
                fillMats()
                applyPanoMats()
                goodselection = False

                # join masked
                if cb_protectfacemask and hasFaces == True:
                    splitobj.select_set(True)  # Select the object
                    obj.select_set(True)  # Select the object
                    context.view_layer.objects.active = obj
                    bpy.ops.object.join()

                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.remove_doubles()
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.object.mode_set(mode='OBJECT')

            else:
                self.report(
                    {'WARNING'}, 'Something went wrong.. Check your selection!')
        else:
            self.report(
                {'WARNING'}, 'Something went wrong.. Check your selection!')

        return {'FINISHED'}


# dollhousebake
class PCAPLUS_OT_dollhousebake(bpy.types.Operator):
    """Bake dollhouse texture"""
    bl_idname = "pcaplus.dollhousebake"
    bl_label = "bake uv texture"
    bl_options = {'UNDO'}

    def execute(self, context):

        createuv = context.scene.cb_createuv

        bakeimgname = context.scene.bakeimgname
        bakeimgname = cleanstr(bakeimgname)
        bakeimgsize = context.scene.bakeimgsize

        obj = bpy.context.active_object
        bpy.ops.object.select_all(action='DESELECT')

        obj.select_set(True)  # Select the object
        # Set the object as the active object
        bpy.context.view_layer.objects.active = obj

        if obj.type == 'MESH' and len(obj.material_slots) > 0:

            # check UVs / create
            if createuv:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles()
                bpy.ops.uv.smart_project(
                    island_margin=0.005, scale_to_bounds=False)
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')

            if not obj.data.uv_layers:
                self.report({'WARNING'}, 'Mesh has no UV layout..')

            else:
                # remove unused materials
                bpy.ops.object.material_slot_remove_unused()

                # remove image if exist
                for i in bpy.data.images:
                    if i.name == bakeimgname:
                        bpy.data.images.remove(i)

                # create new image
                bpy.ops.image.new(name=bakeimgname, width=bakeimgsize, height=bakeimgsize, color=(
                    0.0, 0.0, 0.0, 1.0), alpha=True, generated_type='BLANK')

                # add/select PCA_BAKE_NODE
                for s in obj.material_slots:
                    if s.material and s.material.use_nodes:
                        for node in s.material.node_tree.nodes:
                            if node.label == 'PCA_BAKE_NODE':
                                bakernode = node
                                bakernode.image = bpy.data.images[bakeimgname]
                                bakernode.select = True
                                s.material.node_tree.nodes.active = bakernode
                                break
                        else:
                            bakernode = s.material.node_tree.nodes.new(
                                type="ShaderNodeTexImage")
                            bakernode.label = 'PCA_BAKE_NODE'
                            bakernode.name = 'PCA_BAKE_NODE'
                            bakernode.color = (0.409088, 0, 0.358597)
                            bakernode.use_custom_color = True
                            bakernode.image = bpy.data.images[bakeimgname]
                            bakernode.select = True
                            s.material.node_tree.nodes.active = bakernode

                # render settings
                bpy.context.scene.render.engine = 'CYCLES'
                bpy.context.scene.cycles.samples = 1
                bpy.context.scene.cycles.bake_type = 'EMIT'
                bpy.context.scene.cycles.use_denoising = False
                # bake
                bpy.ops.object.bake(type='EMIT')

        else:
            self.report(
                {'WARNING'}, 'Something went wrong.. Check your selection!')

        return {'FINISHED'}
