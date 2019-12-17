# __init__.py
#
# This file is part of Kuesa.
#
# Copyright (C) 2018 Klarälvdalens Datakonsult AB, a KDAB Group company, info@kdab.com
# Author: Timo Buske <timo.buske@kdab.com>
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
from .Layers.KDAB_kuesa_layers import KDAB_kuesa_layers_properties, GLTF_PT_KDAB_kuesa_layers

bl_info = {
    "name": "KDAB - Kuesa Tools For Blender",
    "author": "Timo Buske <timo.buske@kdab.com>, Juan Casafranca <juan.casafranca@kdab.com>",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "description": "KDAB - Kuesa Tools For Blender",
    "category": "All"
}


glTF2ExportUserExtensions = [Layers.KDAB_kuesa_layers.KDAB_kuesa_layers]


def register():
    # Register layer classes with Blender
    bpy.utils.register_class(KDAB_kuesa_layers_properties)
    bpy.types.Scene.KDAB_kuesa_layers_properties = bpy.props.PointerProperty(type=KDAB_kuesa_layers_properties)


def register_panel():
    try:
        bpy.utils.register_class(GLTF_PT_KDAB_kuesa_layers)
    except Exception:
        pass

    return unregister_panel


def unregister():
    unregister_panel()
    bpy.utils.unregister_class(KDAB_kuesa_layers_properties)
    del bpy.types.Scene.KDAB_kuesa_layers_properties


def unregister_panel():
    # Since panel is registered on demand, it is possible it is not registered
    try:
        bpy.utils.unregister_class(GLTF_PT_KDAB_kuesa_layers)
    except Exception:
        pass

if __name__ == "__main__":
    register()
