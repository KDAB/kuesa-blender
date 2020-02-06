
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

class IroNormal(bpy.types.ShaderNodeCustomGroup):

    bl_name='IroNormal'
    bl_label='Iro Normal'

    # Setup the node - setup the node tree and add the group Input and Output nodes
    def init(self, context):
        node_tree=bpy.data.node_groups.new('.' + self.bl_name, 'ShaderNodeTree')

        node_tree.inputs.new("NodeSocketVector", "Normal Scaling")
        node_tree.inputs.new("NodeSocketVector", "Normal Disturb")

        node_tree.outputs.new("NodeSocketVector", "Normal")

        gi = node_tree.nodes.new('NodeGroupInput')
        go = node_tree.nodes.new('NodeGroupOutput')

        geometry_node = node_tree.nodes.new("ShaderNodeNewGeometry")

        vector_transform = node_tree.nodes.new("ShaderNodeVectorTransform")
        vector_transform.vector_type = 'NORMAL'
        vector_transform.convert_from = 'WORLD'
        vector_transform.convert_to = 'CAMERA'

        invert_z_component_node = node_tree.nodes.new("ShaderNodeVectorMath")
        invert_z_component_node.operation = 'MULTIPLY'
        invert_z_component_node.inputs[1].default_value[0] = 1
        invert_z_component_node.inputs[1].default_value[1] = 1
        invert_z_component_node.inputs[1].default_value[2] = -1

        scale_by_factor_node = node_tree.nodes.new("ShaderNodeVectorMath")
        scale_by_factor_node.operation = 'MULTIPLY'

        add_normal_and_disturb = node_tree.nodes.new("ShaderNodeVectorMath")
        add_normal_and_disturb.operation = 'ADD'

        normalize_result = node_tree.nodes.new("ShaderNodeVectorMath")
        normalize_result.operation = 'NORMALIZE'

        remove_z_component_node = node_tree.nodes.new("ShaderNodeVectorMath")
        remove_z_component_node.operation = 'MULTIPLY'
        remove_z_component_node.inputs[1].default_value[0] = 1
        remove_z_component_node.inputs[1].default_value[1] = 1
        remove_z_component_node.inputs[1].default_value[2] = 0

        # Create links
        node_tree.links.new(geometry_node.outputs['Normal'], vector_transform.inputs[0])
        node_tree.links.new(vector_transform.outputs[0], invert_z_component_node.inputs[0])
        node_tree.links.new(invert_z_component_node.outputs[0], scale_by_factor_node.inputs[0])
        node_tree.links.new(gi.outputs["Normal Scaling"], scale_by_factor_node.inputs[1])
        node_tree.links.new(gi.outputs["Normal Disturb"], remove_z_component_node.inputs[0])
        node_tree.links.new(scale_by_factor_node.outputs[0], add_normal_and_disturb.inputs[0])
        node_tree.links.new(remove_z_component_node.outputs[0], add_normal_and_disturb.inputs[1])
        node_tree.links.new(add_normal_and_disturb.outputs[0], normalize_result.inputs[0])
        node_tree.links.new(normalize_result.outputs[0], go.inputs["Normal"])

        self.node_tree = node_tree

    # Copy
    def copy(self, node):
        self.node_tree=node.node_tree.copy()

    # Free (when node is deleted)
    def free(self):
        bpy.data.node_groups.remove(self.node_tree, do_unlink=True)

class IroFresnel(bpy.types.ShaderNodeCustomGroup):

    bl_name='IroFresnel'
    bl_label='Iro Fresnel'

    # Setup the node - setup the node tree and add the group Input and Output nodes
    def init(self, context):
        node_tree=bpy.data.node_groups.new('.' + self.bl_name, 'ShaderNodeTree')

        node_tree.inputs.new("NodeSocketVector", "Normal")
        node_tree.outputs.new("NodeSocketFloat", "Fresnel Factor")

        gi = node_tree.nodes.new('NodeGroupInput')
        go = node_tree.nodes.new('NodeGroupOutput')

        separate_xyz = node_tree.nodes.new("ShaderNodeSeparateXYZ")

        subtract_node = node_tree.nodes.new("ShaderNodeMath")
        subtract_node.operation = 'SUBTRACT'
        subtract_node.inputs[0].default_value = 1

        power_2_node = node_tree.nodes.new("ShaderNodeMath")
        power_2_node.operation = 'MULTIPLY'

        # Create links
        node_tree.links.new(gi.outputs["Normal"], separate_xyz.inputs[0])
        node_tree.links.new(separate_xyz.outputs['Z'], subtract_node.inputs[1])
        node_tree.links.new(subtract_node.outputs[0], power_2_node.inputs[0])
        node_tree.links.new(subtract_node.outputs[0], power_2_node.inputs[1])
        node_tree.links.new(power_2_node.outputs[0], go.inputs["Fresnel Factor"])

        self.node_tree = node_tree

    # Copy
    def copy(self, node):
        self.node_tree=node.node_tree.copy()

    # Free (when node is deleted)
    def free(self):
        bpy.data.node_groups.remove(self.node_tree, do_unlink=True)

class IroS(bpy.types.ShaderNodeCustomGroup):

    bl_name='IroS'
    bl_label='Iro S'

    # Setup the node - setup the node tree and add the group Input and Output nodes
    def init(self, context):
        node_tree=bpy.data.node_groups.new('.' + self.bl_name, 'ShaderNodeTree')

        node_tree.inputs.new("NodeSocketVector", "Normal")
        node_tree.outputs.new("NodeSocketVector", "Environment UV")

        gi = node_tree.nodes.new('NodeGroupInput')
        go = node_tree.nodes.new('NodeGroupOutput')

        multiply_node = node_tree.nodes.new("ShaderNodeVectorMath")
        multiply_node.operation = 'MULTIPLY'
        multiply_node.inputs[1].default_value[0] = 0.5
        multiply_node.inputs[1].default_value[1] = 0.5
        multiply_node.inputs[1].default_value[2] = 0

        add_node = node_tree.nodes.new("ShaderNodeVectorMath")
        add_node.operation = 'ADD'
        add_node.inputs[1].default_value[0] = 0.5
        add_node.inputs[1].default_value[1] = 0.5
        add_node.inputs[1].default_value[2] = 0

        # Create links
        node_tree.links.new(gi.outputs["Normal"], multiply_node.inputs[0])
        node_tree.links.new(multiply_node.outputs[0], add_node.inputs[0])
        node_tree.links.new(add_node.outputs[0], go.inputs["Environment UV"])

        self.node_tree = node_tree

    # Copy
    def copy(self, node):
        self.node_tree=node.node_tree.copy()

    # Free (when node is deleted)
    def free(self):
        bpy.data.node_groups.remove(self.node_tree, do_unlink=True)

class IroPostVertexColor(bpy.types.ShaderNodeCustomGroup):

    bl_name='IroPostVertexColor'
    bl_label='Iro Post Vertex Color'

    # Setup the node - setup the node tree and add the group Input and Output nodes
    def init(self, context):
        node_tree=bpy.data.node_groups.new('.' + self.bl_name, 'ShaderNodeTree')

        node_tree.inputs.new("NodeSocketVector", "Post Vertex Color")
        node_tree.inputs.new("NodeSocketVector", "Post Gain")
        node_tree.outputs.new("NodeSocketVector", "Post Color")

        gi = node_tree.nodes.new('NodeGroupInput')
        go = node_tree.nodes.new('NodeGroupOutput')

        mix_node = node_tree.nodes.new("ShaderNodeMixRGB")
        mix_node.blend_type = 'MIX'
        mix_node.inputs[1].default_value[0] = 1
        mix_node.inputs[1].default_value[1] = 1
        mix_node.inputs[1].default_value[2] = 1
        mix_node.inputs[1].default_value[3] = 1

        vertex_color_node = node_tree.nodes.new("ShaderNodeVertexColor")

        multiply_node = node_tree.nodes.new("ShaderNodeVectorMath")
        multiply_node.operation = 'MULTIPLY'

        combine_node = node_tree.nodes.new("ShaderNodeCombineXYZ")

        # Create links
        node_tree.links.new(gi.outputs["Post Vertex Color"], mix_node.inputs[0])
        node_tree.links.new(vertex_color_node.outputs[0], mix_node.inputs[2])
        node_tree.links.new(gi.outputs["Post Gain"], combine_node.inputs[0])
        node_tree.links.new(gi.outputs["Post Gain"], combine_node.inputs[1])
        node_tree.links.new(gi.outputs["Post Gain"], combine_node.inputs[2])
        node_tree.links.new(mix_node.outputs[0], multiply_node.inputs[0])
        node_tree.links.new(combine_node.outputs[0], multiply_node.inputs[1])
        node_tree.links.new(multiply_node.outputs[0], go.inputs["Post Color"])

        self.node_tree = node_tree

    # Copy
    def copy(self, node):
        self.node_tree=node.node_tree.copy()

    # Free (when node is deleted)
    def free(self):
        bpy.data.node_groups.remove(self.node_tree, do_unlink=True)
