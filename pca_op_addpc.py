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
import os
from bpy_extras.io_utils import ImportHelper
from . pca_funcs import cleanstr, check_if_faces


class PCAPLUS_OT_addpcop(bpy.types.Operator, ImportHelper):
    """Open the 'Add PanoCam' dialog box"""
    bl_label = "OK"
    bl_idname = "pcaplus.addpcop"
    bl_options = {'UNDO'}

    filter_glob: bpy.props.StringProperty(
        default='*.jpg;*.JPG;*.jpeg;*.png;*.tif;*.tiff',
        options={'HIDDEN'}
    )  # type: ignore

    material_boolean: bpy.props.BoolProperty(
        name='Create PanoMAT',
        description='create panomaterial and background world',
        default=True,
    )  # type: ignore

    facemask_boolean: bpy.props.BoolProperty(
        name='Protect Vertex Group',
        description='',
        default=False,
    )  # type: ignore

    pname: bpy.props.StringProperty(
        name='Name: ',
        description='Leave blank to automatically apply the image name',
        default=''
    )  # type: ignore

    cheight: bpy.props.FloatProperty(
        name="Camera Height: ",
        description='Height above the 3D-cursor',
        soft_min=0, soft_max=1500,
        default=1.65
    )  # type: ignore

    def execute(self, context):
        """  """

        hasFaces = False

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

        filename, extension = os.path.splitext(self.filepath)
        imgname = os.path.splitext(
            os.path.basename(f'{filename}{extension}'))[0]

        obj = bpy.context.active_object

        # check selected objects
        ol = 0
        if len(bpy.context.selected_objects) > 0:
            ol = 1
            obj = bpy.context.selected_objects[0]

        # remove materials
        creatematerial = self.material_boolean

        if creatematerial == True:
            if extension != '.jpg' and extension != '.JPG' and extension != '.jpeg' and extension != '.png' and extension != '.tif' and extension != '.tiff':
                self.report(
                    {'WARNING'}, 'Only jpg, png or tif images allowed!')
                return {'FINISHED'}

            if obj != None and obj.type == 'MESH':
                if self.facemask_boolean and len(obj.vertex_groups) > 0:
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='DESELECT')

                    # select vertex group, switch to edge and face mode
                    bpy.ops.object.vertex_group_select()
                    bpy.ops.mesh.select_mode(
                        use_extend=False, use_expand=False, type='EDGE')
                    bpy.ops.mesh.select_mode(
                        use_extend=False, use_expand=False, type='FACE')

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

            # remove all materials
            if ol == 1 and obj.type == 'MESH':
                for s in range(len(obj.material_slots)):
                    obj.active_material_index = 0
                    bpy.ops.object.material_slot_remove()

        camheight = self.cheight
        imgpath = str(self.filepath)
        pn = str(self.pname)
        pn = cleanstr(pn)

        # name = imagename
        if creatematerial == True and pn == '':
            pn = imgname

        if pn == '':
            self.report({'WARNING'}, "Enter a name or select an image")
            return {'FINISHED'}

        # add Panoempty
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        bpy.context.object.name = pn + "_HANDLE"

        pemty = bpy.context.active_object
        pemty.location[2] += camheight
        pemty.show_name = True

        # add Cam360
        bpy.ops.object.camera_add(
            enter_editmode=False, align='WORLD', rotation=(1.5708, 0, 0))
        pcam = bpy.context.active_object

        pcam.data.lens_unit = 'MILLIMETERS'
        pcam.data.lens = 18
        pcam.name = pn + "_CAM"
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

        # add rotempty
        bpy.ops.object.empty_add(type='SPHERE', location=(0, 0, 0))
        prot = bpy.context.active_object
        prot.empty_display_size = 0.1
        prot.name = pn + "_ROT"
        prot.lock_location[0] = True
        prot.lock_location[1] = True
        prot.lock_location[2] = True
        bpy.ops.object.constraint_add(type='COPY_ROTATION')
        bpy.context.object.constraints["Copy Rotation"].target = pemty

        # create material
        if creatematerial == True:

            # add mat
            pmat = bpy.data.materials.new(name="new")
            pmat.use_nodes = True
            pmat.use_fake_user = True
            pmat.name = pn + "_MAT"

            # Remove default material
            # title of the existing node when materials.new
            pmat.node_tree.nodes.remove(
                pmat.node_tree.nodes.get('Principled BSDF'))
            pmat_output = pmat.node_tree.nodes.get('Material Output')

            # ADD PANO NODE GROUP
            pano_group_node = pmat.node_tree.nodes.new(type='ShaderNodeGroup')
            pano_group_node.node_tree = create_pano_node_group(
                f'{pn}_GROUP', pemty)
            # Link the group to the output
            pmat.node_tree.links.new(
                pano_group_node.outputs[0], pmat_output.inputs[0])

            # backface culling
            pmat.use_backface_culling = True

            # apply MAT
            if ol == 1:
                if obj.type == 'MESH':
                    obj.active_material = pmat

            #
            # Create PanoWorld
            #
            pworld = bpy.data.worlds.new(name="new")
            pworld.use_nodes = True
            pworld.use_fake_user = True
            pworld.name = pn + "_WORLD"

            # Environment
            pano_node = pworld.node_tree.nodes.new('ShaderNodeTexEnvironment')
            pano_node.label = "Panorama"
            pano_node.image = bpy.data.images.load(imgpath)
            pano_node.location = (-400, 500)

            # hue saturation
            panobw_node = pworld.node_tree.nodes.new('ShaderNodeHueSaturation')
            panobw_node.inputs[1].default_value = 0
            panobw_node.location = (-100, 500)
            panobw_node.inputs[4].show_expanded = True

            # mapping
            pano_m_node2 = pworld.node_tree.nodes.new('ShaderNodeMapping')
            pano_m_node2.label = "Pre Leveling Panorama"
            pano_m_node2.name = "PanoMapping02"
            pano_m_node2.inputs[2].default_value[2] = -1.5708
            pano_m_node2.location = (-800, 300)

            # Texture Coordinate
            pano_co_node = pworld.node_tree.nodes.new('ShaderNodeTexCoord')
            pano_co_node.location = (-1000, 300)
            pano_co_node.object = prot

            background_node = pworld.node_tree.nodes["Background"]
            background_node.inputs[0].show_expanded = True

            # Creating Links between the Nodes
            pworld.node_tree.links.new(
                pano_co_node.outputs[3], pano_m_node2.inputs[0])
            pworld.node_tree.links.new(
                pano_m_node2.outputs[0], pano_node.inputs[0])
            pworld.node_tree.links.new(
                pano_node.outputs[0], panobw_node.inputs[4])
            pworld.node_tree.links.new(
                panobw_node.outputs[0], background_node.inputs[0])

            # activate new world
            bpy.context.scene.world = pworld

            if self.facemask_boolean and hasFaces == True:
                splitobj.select_set(True)  # Select the object
                obj.select_set(True)  # Select the object
                context.view_layer.objects.active = obj
                bpy.ops.object.join()
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles()
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')

            self.report({'INFO'}, 'PanoCam, material and world created.')

        bpy.ops.object.select_all(action='DESELECT')

        pemty.select_set(True)
        bpy.context.view_layer.objects.active = pemty

        return {'FINISHED'}
