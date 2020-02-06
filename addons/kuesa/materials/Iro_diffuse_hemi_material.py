# This file is part of Kuesa.
#
# Copyright (C) 2019 Klarälvdalens Datakonsult AB, a KDAB Group company, info@kdab.com
# Author: Juan Casafranca <juan.casafranca@kdab.com>
#
# Licensees holding valid proprietary KDAB Kuesa licenses may use this file in
# accordance with the Kuesa Enterprise License Agreement provided with the Software in the
# LICENSE.KUESA.ENTERPRISE file.
#
# Contact info@kdab.com if any conditions of this licensing are not clear to you.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bpy
import os

class IroDiffuseHemi(bpy.types.ShaderNodeCustomGroup):

    bl_name='IroDiffuseHemiMaterial'
    bl_label='Iro Diffuse Hemi Material'

    def init(self, context):
        print("init")
        self.create_tree()

    def copy(self, node):
        print("copy")
        self.create_tree()

    def free(self):
        for node in self.node_tree.nodes:
            try:
                node.free()
            except Exception:
                pass
        bpy.data.node_groups.remove(self.node_tree, do_unlink=True)

    def create_tree(self):
        node_tree=bpy.data.node_groups.new('.' + self.bl_name, 'ShaderNodeTree')

        # Create node interface
        node_tree.inputs.new("NodeSocketVector", "Normal Scaling")
        node_tree.inputs.new("NodeSocketVector", "Normal Disturb")
        node_tree.inputs.new("NodeSocketFloat", "Reflection Gain")
        node_tree.inputs.new("NodeSocketColor", "Reflection Inner Filter")
        node_tree.inputs.new("NodeSocketColor", "Reflection Outer Filter")
        node_tree.inputs.new("NodeSocketFloat", "Diffuse Gain")
        node_tree.inputs.new("NodeSocketColor", "Diffuse Inner Filter")
        node_tree.inputs.new("NodeSocketColor", "Diffuse Outer Filter")
        node_tree.inputs.new("NodeSocketFloat", "Post Vertex Color")
        node_tree.inputs.new("NodeSocketFloat", "Post Gain")
        node_tree.inputs.new("NodeSocketColor", "Post Hemi Filter")

        node_tree.outputs.new("NodeSocketColor", "Color")

        gi = node_tree.nodes.new('NodeGroupInput')
        go = node_tree.nodes.new('NodeGroupOutput')

        node_tree.inputs["Normal Scaling"].default_value[0] = 1
        node_tree.inputs["Normal Scaling"].default_value[1] = 1
        node_tree.inputs["Normal Scaling"].default_value[2] = 1
        node_tree.inputs["Reflection Gain"].default_value = 1
        node_tree.inputs["Reflection Inner Filter"].default_value[0] = 1
        node_tree.inputs["Reflection Inner Filter"].default_value[1] = 1
        node_tree.inputs["Reflection Inner Filter"].default_value[2] = 1
        node_tree.inputs["Reflection Inner Filter"].default_value[3] = 1
        node_tree.inputs["Reflection Outer Filter"].default_value[0] = 1
        node_tree.inputs["Reflection Outer Filter"].default_value[1] = 1
        node_tree.inputs["Reflection Outer Filter"].default_value[2] = 1
        node_tree.inputs["Reflection Outer Filter"].default_value[3] = 1
        node_tree.inputs["Diffuse Gain"].default_value = 1
        node_tree.inputs["Diffuse Inner Filter"].default_value[0] = 1
        node_tree.inputs["Diffuse Inner Filter"].default_value[1] = 1
        node_tree.inputs["Diffuse Inner Filter"].default_value[2] = 1
        node_tree.inputs["Diffuse Inner Filter"].default_value[3] = 1
        node_tree.inputs["Diffuse Outer Filter"].default_value[0] = 1
        node_tree.inputs["Diffuse Outer Filter"].default_value[1] = 1
        node_tree.inputs["Diffuse Outer Filter"].default_value[2] = 1
        node_tree.inputs["Diffuse Outer Filter"].default_value[3] = 1
        node_tree.inputs["Post Vertex Color"].default_value = 0
        node_tree.inputs["Post Gain"].default_value = 1
        node_tree.inputs["Post Hemi Filter"].default_value[0] = 0
        node_tree.inputs["Post Hemi Filter"].default_value[1] = 0
        node_tree.inputs["Post Hemi Filter"].default_value[2] = 0
        node_tree.inputs["Post Hemi Filter"].default_value[3] = 0

        # Create nodes and configure default values
        iro_diffuse_node = node_tree.nodes.new("IroDiffuse")

        multiply_color_by_hemi_node = node_tree.nodes.new("ShaderNodeVectorMath")
        multiply_color_by_hemi_node.operation = 'MULTIPLY'
        geometry_node = node_tree.nodes.new("ShaderNodeNewGeometry")
        separate_xyz_node = node_tree.nodes.new("ShaderNodeSeparateXYZ")
        invert_z_node = node_tree.nodes.new("ShaderNodeMath")
        invert_z_node.operation = 'MULTIPLY'
        invert_z_node.inputs[1].default_value = -1
        clamp_node = node_tree.nodes.new("ShaderNodeClamp")
        mix_node = node_tree.nodes.new("ShaderNodeMixRGB")
        mix_node.inputs[1].default_value = [1,1,1,1]

        # Create links
        node_tree.links.new(geometry_node.outputs["Normal"], separate_xyz_node.inputs[0])
        node_tree.links.new(separate_xyz_node.outputs['Z'], invert_z_node.inputs[0])
        node_tree.links.new(invert_z_node.outputs[0], clamp_node.inputs[0])
        node_tree.links.new(clamp_node.outputs[0], mix_node.inputs[0])
        node_tree.links.new(gi.outputs["Post Hemi Filter"], mix_node.inputs[2])

        node_tree.links.new(iro_diffuse_node.outputs["Color"], multiply_color_by_hemi_node.inputs[1])
        node_tree.links.new(mix_node.outputs[0], multiply_color_by_hemi_node.inputs[0])
        node_tree.links.new(multiply_color_by_hemi_node.outputs[0], go.inputs["Color"])

        node_tree.links.new(multiply_color_by_hemi_node.outputs[0], go.inputs["Color"])

        for output_socket in gi.outputs:
            try:
                input_socket = iro_diffuse_node.inputs[output_socket.name]
                node_tree.links.new(output_socket, input_socket)
            except Exception:
                pass

        self.node_tree = node_tree

    # Draw the node components
    def draw_buttons(self, context, layout):

        node_tree = self.node_tree.nodes["Iro Diffuse Material"].node_tree

        env_texture = node_tree.nodes["EnvTexture"]
        box = layout.box()
        box.label(text="Environment map")
        box.template_ID(env_texture, "image", new="image.new", open="image.open")

        diffuse_texture = node_tree.nodes["DiffuseTexture"]
        box = layout.box()
        box.label(text="Diffuse map")
        box.template_ID(diffuse_texture, "image", new="image.new", open="image.open")

        env_multiply_filter = node_tree.nodes["EnvMultiply"]
        env_texture_output = env_texture.outputs["Color"]
        env_color_input = env_multiply_filter.inputs[1]

        if env_texture.image is not None:
            if not len(env_texture_output.links):
                node_tree.links.new(env_texture_output, env_color_input)
        else:
            for link in env_texture_output.links:
                node_tree.links.remove(link)

        diffuse_multiply_filter = node_tree.nodes["DiffuseMultiply"]
        diffuse_texture_output = diffuse_texture.outputs["Color"]
        diffuse_color_input = diffuse_multiply_filter.inputs[1]

        if diffuse_texture.image is not None:
            if not len(diffuse_texture_output.links):
                node_tree.links.new(diffuse_texture_output, diffuse_color_input)
        else:
            for link in diffuse_texture_output.links:
                node_tree.links.remove(link)