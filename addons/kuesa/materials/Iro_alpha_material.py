# This file is part of Kuesa.
#
# Copyright (C) 2020 Klarälvdalens Datakonsult AB, a KDAB Group company, info@kdab.com
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

class IroAlpha(bpy.types.ShaderNodeCustomGroup):

    bl_name='IroAlphaMaterial'
    bl_label='Iro Alpha Material'

    # Setup the node - setup the node tree and add the group Input and Output nodes
    def init(self, context):
        filepath = os.path.dirname(__file__) + "/materials.blend/NodeTree/"
        bpy.ops.wm.append(filename=".KDAB_custom_material_Iro_alpha_template", directory=filepath)
        self.node_tree = bpy.data.node_groups[".KDAB_custom_material_Iro_alpha_template"]
        self.node_tree.name = ".KDAB_custom_material_internal_Iro_alpha"

    # Draw the node components
    def draw_buttons(self, context, layout):
        env = self.node_tree.nodes["env"]
        box = layout.box()
        box.label(text="Environment map")
        box.template_ID(env, "image", new="image.new", open="image.open")

    # Copy
    def copy(self, node):
        self.node_tree=node.node_tree.copy()

    # Free (when node is deleted)
    def free(self):
        bpy.data.node_groups.remove(self.node_tree, do_unlink=True)
