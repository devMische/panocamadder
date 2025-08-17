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
import operator

ops = {"+": operator.add,
       "-": operator.sub,
       "*": operator.mul,
       "/": operator.truediv}


def removeImgExtension(string):
    return string.rsplit('.', 1)[0]


def addpci(pano, location, rotation):

    panoname = removeImgExtension(pano)
    model = bpy.context.active_object
    imgpath = f'{bpy.types.Scene.jsonpath}/{pano}'
    rad_or_deg = bpy.context.scene.rad_or_deg
    exist = False

    # create pano node group
    def create_pano_node_group(name, empty):

        # Create new node group
        group = bpy.data.node_groups.new(f'{name}', 'ShaderNodeTree')

        # Define interface
        mixshader_input = group.interface.new_socket(
            name="Mix",
            description="Mix shaders",
            in_out='INPUT',
            socket_type='NodeSocketFloat'
        )
        mixshader_input.min_value = 0
        mixshader_input.max_value = 1
        mixshader_input.default_value = 1

        shader_input = group.interface.new_socket(
            name="Pano_GROUP",
            description="Pano group input",
            in_out='INPUT',
            socket_type='NodeSocketShader'
        )

        shader_output = group.interface.new_socket(
            name="Emission",
            description="Shader output",
            in_out='OUTPUT',
            socket_type='NodeSocketShader'
        )

        # Create nodes
        nodes = group.nodes

        group_in = nodes.new(type='NodeGroupInput')
        group_in.location = (-900, 0)

        group_out = nodes.new(type='NodeGroupOutput')
        group_out.location = (400, 0)

        # mix shader
        texslider_node = nodes.new('ShaderNodeMixShader')
        texslider_node.label = "MIXER"
        texslider_node.location = (130, 50)
        texslider_node.inputs[0].default_value = 1
        texslider_node.inputs[2].show_expanded = True

        # emission shader
        panoemi_node = nodes.new('ShaderNodeEmission')
        panoemi_node.location = (-30, 200)
        panoemi_node.inputs[0].show_expanded = True

        # Environment Texture
        panotex_node = nodes.new('ShaderNodeTexEnvironment')
        panotex_node.label = "Panorama"
        panotex_node.image = bpy.data.images.load(imgpath)
        panotex_node.location = (-300, 200)

        # mapping
        panotexm2_node = nodes.new('ShaderNodeMapping')
        panotexm2_node.label = "Pre Leveling Panorama"
        panotexm2_node.name = "PanoTexMapping02"
        panotexm2_node.inputs[2].default_value[2] = -1.5708
        panotexm2_node.location = (-500, 300)

        # Texture Coordinate
        panotex_co_node = nodes.new('ShaderNodeTexCoord')
        panotex_co_node.location = (-700, 300)
        panotex_co_node.object = empty

        # Create links
        links = group.links
        links.new(panoemi_node.outputs[0], texslider_node.inputs[2])
        links.new(texslider_node.outputs[0], group_out.inputs[0])
        links.new(texslider_node.inputs[0], group_in.outputs[0])
        links.new(texslider_node.inputs[1], group_in.outputs[1])
        links.new(panotex_node.outputs[0], panoemi_node.inputs[0])
        links.new(panotex_co_node.outputs[3], panotexm2_node.inputs[0])
        links.new(panotexm2_node.outputs[0], panotex_node.inputs[0])

        return group

    for o in bpy.context.scene.objects:

        if o.name == panoname + '_HANDLE':

            exist = True

    if exist == True:
        # move existing Panoempty
        pemty = bpy.data.objects[panoname + '_HANDLE']
        pemty.location[0] = location[0]
        pemty.location[1] = location[1]
        pemty.location[2] = location[2]

        if rad_or_deg == "degrees":
            pemty.rotation_euler[0] = math.radians(rotation[0])
            pemty.rotation_euler[1] = math.radians(rotation[1])
            pemty.rotation_euler[2] = math.radians(rotation[2])
        else:
            pemty.rotation_euler[0] = rotation[0]
            pemty.rotation_euler[1] = rotation[1]
            pemty.rotation_euler[2] = rotation[2]

        if model != None and model.type == "MESH" and f'{panoname}_MAT' in bpy.data.materials:

            model.select_set(True)  # Select the object
            # Set the object as the active object
            bpy.context.view_layer.objects.active = model

            for i in range(len(model.material_slots)):
                model.active_material_index = 0
                bpy.ops.object.material_slot_remove()

            model.active_material = bpy.data.materials[panoname + "_MAT"]

    else:
        # add Panoempty
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        bpy.context.object.name = panoname + '_HANDLE'

        pemty = bpy.context.active_object
        pemty.location[0] = location[0]
        pemty.location[1] = location[1]
        pemty.location[2] = location[2]

        if rad_or_deg == "degrees":
            pemty.rotation_euler[0] = math.radians(rotation[0])
            pemty.rotation_euler[1] = math.radians(rotation[1])
            pemty.rotation_euler[2] = math.radians(rotation[2])
        else:
            pemty.rotation_euler[0] = rotation[0]
            pemty.rotation_euler[1] = rotation[1]
            pemty.rotation_euler[2] = rotation[2]

        pemty.show_name = True

        # add Cam360
        bpy.ops.object.camera_add(
            enter_editmode=False, align='WORLD', rotation=(1.5708, 0, 0))
        pcam = bpy.context.active_object

        pcam.data.lens_unit = 'MILLIMETERS'
        pcam.data.lens = 18
        pcam.name = panoname + "_CAM"
        pcam.data.show_name = True
        pcam.data.show_passepartout = False
        bpy.ops.object.constraint_add(type='COPY_LOCATION')
        bpy.context.object.constraints["Copy Location"].target = pemty

        pcam.lock_location[0] = True
        pcam.lock_location[1] = True
        pcam.lock_location[2] = True
        pcam.lock_rotation[1] = True
        bpy.context.space_data.lock_camera = True
        bpy.context.space_data.camera = pcam

        # add mat

        pmat = bpy.data.materials.new(name="new")
        pmat.use_nodes = True
        pmat.use_fake_user = True
        pmat.name = panoname + "_MAT"

        # Remove default material
        # title of the existing node when materials.new
        pmat.node_tree.nodes.remove(
            pmat.node_tree.nodes.get('Principled BSDF'))
        pmat_output = pmat.node_tree.nodes.get('Material Output')

        # ADD PANO NODE GROUP
        pano_group_node = pmat.node_tree.nodes.new(type='ShaderNodeGroup')
        pano_group_node.node_tree = create_pano_node_group(
            f'{panoname}_GROUP', pemty)
        # Link the group to the output
        pmat.node_tree.links.new(
            pano_group_node.outputs[0], pmat_output.inputs[0])

        # backface culling
        pmat.use_backface_culling = True

        if model != None and model.type == "MESH":

            model.select_set(True)  # Select the object
            # Set the object as the active object
            bpy.context.view_layer.objects.active = model

            for i in range(len(model.material_slots)):
                model.active_material_index = 0
                bpy.ops.object.material_slot_remove()

            model.active_material = pmat


class PCA_OT_createallpci(bpy.types.Operator):
    """ Create all PanoCams """
    bl_label = "Create/Update all"
    bl_idname = "pca.createallpci"
    bl_options = {'UNDO'}

    def execute(self, context):
        """ Create all PanoCams """

        pcijson = context.scene.pcijson

        json_loc_x = int(context.scene.json_loc_x)
        json_loc_y = int(context.scene.json_loc_y)
        json_loc_z = int(context.scene.json_loc_z)

        json_rot_x = int(context.scene.json_rot_x)
        json_rot_y = int(context.scene.json_rot_y)
        json_rot_z = int(context.scene.json_rot_z)

        loc_x_operator = context.scene.loc_x_operator
        loc_y_operator = context.scene.loc_y_operator
        loc_z_operator = context.scene.loc_z_operator

        rot_x_operator = context.scene.rot_x_operator
        rot_y_operator = context.scene.rot_y_operator
        rot_z_operator = context.scene.rot_z_operator

        loc_x_nmbr = context.scene.loc_x_nmbr
        loc_y_nmbr = context.scene.loc_y_nmbr
        loc_z_nmbr = context.scene.loc_z_nmbr

        rot_x_nmbr = context.scene.rot_x_nmbr
        rot_y_nmbr = context.scene.rot_y_nmbr
        rot_z_nmbr = context.scene.rot_z_nmbr

        for item in pcijson:
            if context.scene.loc_x_operator != 'no':
                loc_x = round(ops[loc_x_operator](
                    item['location'][json_loc_x], loc_x_nmbr), 6)
            else:
                loc_x = item['location'][json_loc_x]

            if context.scene.loc_y_operator != 'no':
                loc_y = round(ops[loc_y_operator](
                    item['location'][json_loc_y], loc_y_nmbr), 6)
            else:
                loc_y = item['location'][json_loc_y]

            if context.scene.loc_z_operator != 'no':
                loc_z = round(ops[loc_z_operator](
                    item['location'][json_loc_z], loc_z_nmbr), 6)
            else:
                loc_z = item['location'][json_loc_z]

            location = (loc_x, loc_y, loc_z)

            if context.scene.rot_x_operator != 'no':
                rot_x = round(ops[rot_x_operator](
                    item['rotation'][json_rot_x], rot_x_nmbr), 6)
            else:
                rot_x = item['rotation'][json_rot_x]
            if context.scene.rot_y_operator != 'no':
                rot_y = round(ops[rot_y_operator](
                    item['rotation'][json_rot_y], rot_y_nmbr), 6)
            else:
                rot_y = item['rotation'][json_rot_y]
            if context.scene.rot_z_operator != 'no':
                rot_z = round(ops[rot_z_operator](
                    item['rotation'][json_rot_z], rot_z_nmbr), 6)
            else:
                rot_z = item['rotation'][json_rot_z]

            rotation = (rot_x, rot_y, rot_z)

            addpci(item['pano'], location, rotation)

        return {'FINISHED'}


class PCA_OT_createsinglepci(bpy.types.Operator):
    """ Create current PanoCam """
    bl_label = "Create/Update"
    bl_idname = "pca.createsinglepci"
    bl_options = {'UNDO'}

    def execute(self, context):
        """ Create current PanoCam """

        pcijson = context.scene.pcijson
        idx = context.scene.panonmbr - 1

        json_loc_x = int(context.scene.json_loc_x)
        json_loc_y = int(context.scene.json_loc_y)
        json_loc_z = int(context.scene.json_loc_z)

        json_rot_x = int(context.scene.json_rot_x)
        json_rot_y = int(context.scene.json_rot_y)
        json_rot_z = int(context.scene.json_rot_z)

        loc_x_operator = context.scene.loc_x_operator
        loc_y_operator = context.scene.loc_y_operator
        loc_z_operator = context.scene.loc_z_operator

        rot_x_operator = context.scene.rot_x_operator
        rot_y_operator = context.scene.rot_y_operator
        rot_z_operator = context.scene.rot_z_operator

        loc_x_nmbr = context.scene.loc_x_nmbr
        loc_y_nmbr = context.scene.loc_y_nmbr
        loc_z_nmbr = context.scene.loc_z_nmbr

        rot_x_nmbr = context.scene.rot_x_nmbr
        rot_y_nmbr = context.scene.rot_y_nmbr
        rot_z_nmbr = context.scene.rot_z_nmbr

        if loc_x_operator != 'no':
            loc_x = round(ops[loc_x_operator](
                pcijson[idx]['location'][json_loc_x], loc_x_nmbr), 6)
        else:
            loc_x = pcijson[idx]['location'][json_loc_x]
        if loc_y_operator != 'no':
            loc_y = round(ops[loc_y_operator](
                pcijson[idx]['location'][json_loc_y], loc_y_nmbr), 6)
        else:
            loc_y = pcijson[idx]['location'][json_loc_y]
        if loc_z_operator != 'no':
            loc_z = round(ops[loc_z_operator](
                pcijson[idx]['location'][json_loc_z], loc_z_nmbr), 6)
        else:
            loc_z = pcijson[idx]['location'][json_loc_z]

        location = (loc_x, loc_y, loc_z)

        if rot_x_operator != 'no':
            rot_x = round(ops[rot_x_operator](
                pcijson[idx]['rotation'][json_rot_x], rot_x_nmbr), 6)
        else:
            rot_x = pcijson[idx]['rotation'][json_rot_x]
        if rot_y_operator != 'no':
            rot_y = round(ops[rot_y_operator](
                pcijson[idx]['rotation'][json_rot_y], rot_y_nmbr), 6)
        else:
            rot_y = pcijson[idx]['rotation'][json_rot_y]
        if rot_z_operator != 'no':
            rot_z = round(ops[rot_z_operator](
                pcijson[idx]['rotation'][json_rot_z], rot_z_nmbr), 6)
        else:
            rot_z = pcijson[idx]['rotation'][json_rot_z]

        rotation = (rot_x, rot_y, rot_z)

        addpci(pcijson[idx]['pano'], location, rotation)

        return {'FINISHED'}
