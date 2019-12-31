
# KDAB_custom_materials.py
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
import os

from . import Iro_material_common, Iro_diffuse_material, Iro_diffuse_hemi_material, Iro_alpha_material

bl_info = {
    "name": "KDAB_custom_material",
    "category": "glTF 2.0 Extension",
    "blender": (2,80,0),
    'isDraft': False,
    'developer': "KDAB",
    'url': 'https://www.kdab.com',
}

def register_KDAB_custom_materials():
    from nodeitems_utils import NodeItem, register_node_categories, unregister_node_categories
    from nodeitems_builtins import ShaderNodeCategory

    try:
        bpy.utils.register_class(KDAB_custom_materials_properties)
        bpy.types.Scene.KDAB_custom_materials_properties = bpy.props.PointerProperty(type=KDAB_custom_materials_properties)
        bpy.utils.register_class(Iro_material_common.IroNormal)
        bpy.utils.register_class(Iro_material_common.IroFresnel)
        bpy.utils.register_class(Iro_material_common.IroS)
        bpy.utils.register_class(Iro_material_common.IroPostVertexColor)
        bpy.utils.register_class(Iro_diffuse_material.IroDiffuse)
        bpy.utils.register_class(Iro_diffuse_hemi_material.IroDiffuseHemi)
        bpy.utils.register_class(Iro_alpha_material.IroAlpha)
    except Exception:
        pass


    newcatlist = [ShaderNodeCategory("SH_NEW_CUSTOM", "Kuesa", items=[NodeItem("IroDiffuse"), NodeItem("IroDiffuseHemi"), NodeItem("IroAlpha")]),]
    register_node_categories("KUESA_NODES", newcatlist)

def unregister_KDAB_custom_materials():
    from nodeitems_utils import NodeItem, register_node_categories, unregister_node_categories
    from nodeitems_builtins import ShaderNodeCategory
    try:
        unregister_node_categories("KUESA_NODES")
        bpy.utils.unregister_class(Iro_material_common.IroNormal)
        bpy.utils.unregister_class(Iro_material_common.IroFresnel)
        bpy.utils.unregister_class(Iro_material_common.IroS)
        bpy.utils.unregister_class(Iro_material_common.IroPostVertexColor)
        bpy.utils.unregister_class(Iro_diffuse_material.IroDiffuse)
        bpy.utils.unregister_class(KDAB_custom_materials_properties)
        bpy.utils.unregister_class(Iro_diffuse_hemi_material.IroDiffuseHemi)
        bpy.utils.unregister_class(Iro_alpha_material.IroAlpha)
        del bpy.types.Scene.KDAB_custom_materials_properties
    except Exception:
        pass


class KDAB_custom_materials_properties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name='',
        description='',
        default=True
        )



class GLTF_PT_KDAB_custom_materials(bpy.types.Panel):

    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "KDAB_custom_material"
    bl_parent_id = "GLTF_PT_export_user_extensions"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw_header(self, context):
        props = bpy.context.scene.KDAB_custom_materials_properties
        self.layout.prop(props, 'enabled')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        box = layout.box()
        box.label(text="Developer: " + str(bl_info['developer']))
        box.label(text="url: " + str(bl_info['url']))

class KDAB_custom_materials:

    def __init__(self):
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension, ChildOfRootExtension
        from io_scene_gltf2.io.com.gltf2_io import Node
        from io_scene_gltf2.blender.exp.gltf2_blender_gather_texture_info import gather_texture_info
        self.Extension = Extension
        self.ChildOfRootExtension = ChildOfRootExtension
        self.Node = Node
        self.properties = bpy.context.scene.KDAB_custom_materials_properties
        self.gather_texture_info = gather_texture_info

    def gather_material_hook(self, gltf2_material, blender_material, export_settings):
        if self.properties.enabled and blender_material.use_nodes:
            for node in blender_material.node_tree.nodes:
                if isinstance(node, Iro_diffuse_material.IroDiffuse):
                    gltf2_material.extensions[bl_info['name']] = self.Extension(
                        name=bl_info['name'],
                        extension= self.iro_diffuse_extension(node, export_settings),
                        required=False
                    )
                if isinstance(node, Iro_diffuse_hemi_material.IroDiffuseHemi):
                    gltf2_material.extensions[bl_info['name']] = self.Extension(
                        name=bl_info['name'],
                        extension= self.iro_diffuse_hemi_extension(node, export_settings),
                        required=False
                    )

    def iro_diffuse_extension(self, node, export_settings):
        iroDisturb = node.inputs['Iro Disturb XY'].default_value
        iroFactor = node.inputs['Iro Factor'].default_value
        iroInnerFilter = node.inputs['Iro Inner Filter'].default_value
        iroOuterFilter = node.inputs['Iro Outer Filter'].default_value
        diffuseInnerFilter = node.inputs['Diffuse Inner Filter'].default_value
        diffuseOuterFilter = node.inputs['Diffuse Outer Filter'].default_value

        properties = {}
        # The texture is designed to match normals in blender. We need to match the rotation applied!
        if export_settings['gltf_yup']:
            properties["iroFactor"] = [iroFactor[0], -iroFactor[2], iroFactor[1]]
        else:
            properties["iroFactor"] = [iroFactor[0], iroFactor[1], iroFactor[2]]
        properties["iroDisturbXY"] = [iroDisturb[0], iroDisturb[1]]
        properties["postVertexColor"] = node.inputs['Post Vertex Color'].default_value
        properties["postGain"] = node.inputs['Post Gain'].default_value
        properties["iroGain"] = node.inputs["Iro Gain"].default_value
        properties["iroInnerFilter"] = [iroInnerFilter[0], iroInnerFilter[1], iroInnerFilter[2]]
        properties["iroOuterFilter"] = [iroOuterFilter[0], iroOuterFilter[1], iroOuterFilter[2]]
        properties["diffuseInnerFilter"] = [diffuseInnerFilter[0], diffuseInnerFilter[1], diffuseInnerFilter[2]]
        properties["diffuseOuterFilter"] = [diffuseOuterFilter[0], diffuseOuterFilter[1], diffuseOuterFilter[2]]
        properties["diffuseGain"] = node.inputs["Diffuse Gain"].default_value

        env = node.node_tree.nodes["EnvTexture"]
        if env.image is not None:
            env_socket = env.outputs["Color"].links[0].to_socket
            env_info = self.gather_texture_info((env_socket,), export_settings)
            properties["swatchMap"] = env_info

        diffuseTexture = node.node_tree.nodes["DiffuseTexture"]
        if diffuseTexture.image is not None:
            diffuse_socket = diffuseTexture.outputs["Color"].links[0].to_socket
            diffuse_info = self.gather_texture_info((diffuse_socket,), export_settings)
            properties["diffuseMap"] = diffuse_info

        extension = {"type": "IroDiffuse", "properties": properties}

        return extension

    def iro_diffuse_hemi_extension(self, node, export_settings):
        extension = self.iro_diffuse_extension(node.node_tree.nodes["Iro Diffuse Material"], export_settings)
        extension["type"] = "IroDiffuseHemi"
        postHemiFilter = node.inputs["Post Hemi Filter"].default_value
        extension["properties"]["postHemiFilter"] = [postHemiFilter[0], postHemiFilter[1], postHemiFilter[2]]

        return extension
