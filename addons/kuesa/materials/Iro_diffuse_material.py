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

class IroDiffuse(bpy.types.ShaderNodeCustomGroup):

    bl_name='IroDiffuseMaterial'
    bl_label='Iro Diffuse Material'

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
        node_tree.inputs.new("NodeSocketVector", "Iro Factor")
        node_tree.inputs.new("NodeSocketVector", "Iro Disturb XY")
        node_tree.inputs.new("NodeSocketFloat", "Iro Gain")
        node_tree.inputs.new("NodeSocketColor", "Iro Inner Filter")
        node_tree.inputs.new("NodeSocketColor", "Iro Outer Filter")
        node_tree.inputs.new("NodeSocketFloat", "Diffuse Gain")
        node_tree.inputs.new("NodeSocketColor", "Diffuse Inner Filter")
        node_tree.inputs.new("NodeSocketColor", "Diffuse Outer Filter")
        node_tree.inputs.new("NodeSocketFloat", "Post Vertex Color")
        node_tree.inputs.new("NodeSocketFloat", "Post Gain")

        node_tree.outputs.new("NodeSocketColor", "Color")

        gi = node_tree.nodes.new('NodeGroupInput')
        go = node_tree.nodes.new('NodeGroupOutput')

        node_tree.inputs["Iro Factor"].default_value[0] = 1
        node_tree.inputs["Iro Factor"].default_value[1] = 1
        node_tree.inputs["Iro Factor"].default_value[2] = 1
        node_tree.inputs["Iro Gain"].default_value = 1
        node_tree.inputs["Iro Inner Filter"].default_value[0] = 1
        node_tree.inputs["Iro Inner Filter"].default_value[1] = 1
        node_tree.inputs["Iro Inner Filter"].default_value[2] = 1
        node_tree.inputs["Iro Inner Filter"].default_value[3] = 1
        node_tree.inputs["Iro Outer Filter"].default_value[0] = 1
        node_tree.inputs["Iro Outer Filter"].default_value[1] = 1
        node_tree.inputs["Iro Outer Filter"].default_value[2] = 1
        node_tree.inputs["Iro Outer Filter"].default_value[3] = 1
        node_tree.inputs["Diffuse Gain"].default_value = 1
        node_tree.inputs["Iro Inner Filter"].default_value[0] = 1
        node_tree.inputs["Iro Inner Filter"].default_value[1] = 1
        node_tree.inputs["Iro Inner Filter"].default_value[2] = 1
        node_tree.inputs["Iro Inner Filter"].default_value[3] = 1
        node_tree.inputs["Iro Outer Filter"].default_value[0] = 1
        node_tree.inputs["Iro Outer Filter"].default_value[1] = 1
        node_tree.inputs["Iro Outer Filter"].default_value[2] = 1
        node_tree.inputs["Iro Outer Filter"].default_value[3] = 1
        node_tree.inputs["Post Vertex Color"].default_value = 0
        node_tree.inputs["Post Gain"].default_value = 1

        # Create nodes and configure default values
        iro_normal_node = node_tree.nodes.new("IroNormal")
        iro_fresnel_node = node_tree.nodes.new("IroFresnel")
        iro_s_node = node_tree.nodes.new("IroS")
        post_vertex_color_node = node_tree.nodes.new("IroPostVertexColor")

        mix_env_node = node_tree.nodes.new("ShaderNodeMixRGB")
        mix_diffuse_node = node_tree.nodes.new("ShaderNodeMixRGB")
        env_texture = node_tree.nodes.new("ShaderNodeTexImage")
        env_texture.name = "EnvTexture"
        diffuse_texture = node_tree.nodes.new("ShaderNodeTexImage")
        diffuse_texture.name = "DiffuseTexture"

        env_multiply_filter = node_tree.nodes.new("ShaderNodeVectorMath")
        env_multiply_filter.operation = 'MULTIPLY'
        env_multiply_filter.inputs[1].default_value[0] = 1
        env_multiply_filter.inputs[1].default_value[1] = 1
        env_multiply_filter.inputs[1].default_value[2] = 1
        env_multiply_filter.name = "EnvMultiply"

        diffuse_multiply_filter = node_tree.nodes.new("ShaderNodeVectorMath")
        diffuse_multiply_filter.operation = 'MULTIPLY'
        diffuse_multiply_filter.inputs[1].default_value[0] = 0
        diffuse_multiply_filter.inputs[1].default_value[1] = 0
        diffuse_multiply_filter.inputs[1].default_value[2] = 0
        diffuse_multiply_filter.name = "DiffuseMultiply"

        env_gain_vector_node = node_tree.nodes.new("ShaderNodeCombineXYZ")
        diffuse_gain_vector_node = node_tree.nodes.new("ShaderNodeCombineXYZ")

        env_color_node = node_tree.nodes.new("ShaderNodeVectorMath")
        env_color_node.operation = 'MULTIPLY'

        diffuse_color_node = node_tree.nodes.new("ShaderNodeVectorMath")
        diffuse_color_node.operation = 'MULTIPLY'

        add_colors_node = node_tree.nodes.new("ShaderNodeVectorMath")

        multiply_post_vertex_color = node_tree.nodes.new("ShaderNodeVectorMath")
        multiply_post_vertex_color.operation = 'MULTIPLY'

        # Create links
        node_tree.links.new(gi.outputs["Iro Factor"], iro_normal_node.inputs["Iro Factor"])
        node_tree.links.new(gi.outputs["Iro Disturb XY"], iro_normal_node.inputs["Iro Disturb XY"])
        node_tree.links.new(iro_normal_node.outputs["Normal"], iro_fresnel_node.inputs["Normal"])
        node_tree.links.new(iro_normal_node.outputs["Normal"], iro_s_node.inputs["Normal"])
        node_tree.links.new(iro_s_node.outputs["Environment UV"], env_texture.inputs["Vector"])
        node_tree.links.new(iro_fresnel_node.outputs["Fresnel Factor"], mix_diffuse_node.inputs[0])
        node_tree.links.new(gi.outputs["Iro Inner Filter"], mix_env_node.inputs[1])
        node_tree.links.new(gi.outputs["Iro Outer Filter"], mix_env_node.inputs[2])
        node_tree.links.new(iro_fresnel_node.outputs["Fresnel Factor"], mix_env_node.inputs[0])
        node_tree.links.new(gi.outputs["Diffuse Inner Filter"], mix_diffuse_node.inputs[1])
        node_tree.links.new(gi.outputs["Diffuse Outer Filter"], mix_diffuse_node.inputs[2])
        node_tree.links.new(gi.outputs["Iro Gain"], env_gain_vector_node.inputs[0])
        node_tree.links.new(gi.outputs["Iro Gain"], env_gain_vector_node.inputs[1])
        node_tree.links.new(gi.outputs["Iro Gain"], env_gain_vector_node.inputs[2])
        node_tree.links.new(gi.outputs["Diffuse Gain"], diffuse_gain_vector_node.inputs[0])
        node_tree.links.new(gi.outputs["Diffuse Gain"], diffuse_gain_vector_node.inputs[1])
        node_tree.links.new(gi.outputs["Diffuse Gain"], diffuse_gain_vector_node.inputs[2])
        node_tree.links.new(mix_env_node.outputs[0], env_multiply_filter.inputs[0])
        node_tree.links.new(mix_diffuse_node.outputs[0], diffuse_multiply_filter.inputs[0])
        node_tree.links.new(env_multiply_filter.outputs[0], env_color_node.inputs[0])
        node_tree.links.new(env_gain_vector_node.outputs[0], env_color_node.inputs[1])
        node_tree.links.new(diffuse_multiply_filter.outputs[0], diffuse_color_node.inputs[0])
        node_tree.links.new(diffuse_gain_vector_node.outputs[0], diffuse_color_node.inputs[1])
        node_tree.links.new(env_color_node.outputs[0], add_colors_node.inputs[0])
        node_tree.links.new(diffuse_color_node.outputs[0], add_colors_node.inputs[1])
        node_tree.links.new(gi.outputs["Post Vertex Color"], post_vertex_color_node.inputs["Post Vertex Color"])
        node_tree.links.new(gi.outputs["Post Gain"], post_vertex_color_node.inputs["Post Gain"])
        node_tree.links.new(post_vertex_color_node.outputs["Post Color"], multiply_post_vertex_color.inputs[0])
        node_tree.links.new(add_colors_node.outputs[0], multiply_post_vertex_color.inputs[1])
        node_tree.links.new(multiply_post_vertex_color.outputs[0], go.inputs["Color"])

        self.node_tree = node_tree


    # Draw the node components
    def draw_buttons(self, context, layout):
        if self.node_tree is None:
            return
        env_texture = self.node_tree.nodes["EnvTexture"]
        box = layout.box()
        box.label(text="Environment map")
        box.template_ID(env_texture, "image", new="image.new", open="image.open")

        diffuse_texture = self.node_tree.nodes["DiffuseTexture"]
        box = layout.box()
        box.label(text="Diffuse map")
        box.template_ID(diffuse_texture, "image", new="image.new", open="image.open")

        env_multiply_filter = self.node_tree.nodes["EnvMultiply"]
        env_texture_output = env_texture.outputs["Color"]
        env_color_input = env_multiply_filter.inputs[1]

        if env_texture.image is not None:
            if not len(env_texture_output.links):
                self.node_tree.links.new(env_texture_output, env_color_input)
        else:
            for link in env_texture_output.links:
                self.node_tree.links.remove(link)

        diffuse_multiply_filter = self.node_tree.nodes["DiffuseMultiply"]
        diffuse_texture_output = diffuse_texture.outputs["Color"]
        diffuse_color_input = diffuse_multiply_filter.inputs[1]

        if diffuse_texture.image is not None:
            if not len(diffuse_texture_output.links):
                self.node_tree.links.new(diffuse_texture_output, diffuse_color_input)
        else:
            for link in diffuse_texture_output.links:
                self.node_tree.links.remove(link)

