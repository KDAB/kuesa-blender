# KDAB_kuesa_layers.py
#
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

bl_info = {
    "name": "KDAB_kuesa_layers",
    "category": "glTF 2.0 Extension",
    "blender": (2,80,0),
    'isDraft': False,
    'developer': "KDAB",
    'url': 'https://www.kdab.com',
}

class KDAB_kuesa_layers_properties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name='',
        description='',
        default=True
        )

class GLTF_PT_KDAB_kuesa_layers(bpy.types.Panel):

    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "KDAB_kuesa_layers"
    bl_parent_id = "GLTF_PT_export_user_extensions"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw_header(self, context):
        props = bpy.context.scene.KDAB_kuesa_layers_properties
        self.layout.prop(props, 'enabled')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        box = layout.box()
        box.label(text="Developer: " + str(bl_info['developer']))
        box.label(text="url: " + str(bl_info['url']))

class KDAB_kuesa_layers:

    def __init__(self):
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension, ChildOfRootExtension
        from io_scene_gltf2.io.com.gltf2_io import Node
        self.Extension = Extension
        self.ChildOfRootExtension = ChildOfRootExtension
        self.Node = Node
        self.properties = bpy.context.scene.KDAB_kuesa_layers_properties
        self.current_collections = {collection.name : self.ChildOfRootExtension(
                    name=bl_info['name'],
                    path=["layers"],
                    extension=collection.name
                )
                for collection in bpy.data.collections}

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        if self.properties.enabled:

            layers = [self.current_collections[collection.name] for collection in blender_object.users_collection]
            gltf2_object.extensions[bl_info['name']] = self.Extension(
                name=bl_info['name'],
                extension={"layers": layers},
                required=False
            )

