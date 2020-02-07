# Kuesa exporter and tools for Blender

These instructions apply only if you are planning to use Blender 2.79

From Blender 2.80 onward, the glTF exporter provided with Blender is to be used.

The Kuesa exporter for Blender 2.79 provides:

* glTF 2 export
* Kuesa compatible PBR Materials export
* Kuesa layers export as a glTF extension
* Face wireframe export

The Kuesa tools for Blender provide:

* A layer management system allowing to group objects on one or more layers

## Requirements

The Kuesa exporter and tools for Blender requires Blender 2.78 or later

## Components

* The Kuesa tools are bundled in their own addon.
* The Kuesa exporter is a self contained addon.

## Installation

### Prerequisites

It is recommended to disable other glTF export modules in Blender that may conflict with the KDAB provided one.

1. Launch Blender
2. Go to: Files -> User Preferences -> Add-ons
3. In the Add-ons search field, type gltf
4. Deactivate all active entries

### Instructions if you just want to use the addons from prebuilt packages

1. Download the zip files for each addon from http://bit.ly/KuesaForBlender
   * kuesa_latest.zip
   * kuesa_exporter_latest.zip
2. Launch Blender
3. Go to: Files -> User Preferences -> Add-ons -> Install Add-on from File...
4. Search and add each zip file (one at a time)
5. In the Add-ons search field, type kuesa
6. You should now see two entries:
 * All: KDAB - Kuesa Tool for Blender
 * Import-Exporter: KDAB Kuesa glTF format
7. Select them both and hit Save User Settings

### Instructions if you just want to use the addons from sources

1. Clone the repository
2. Move into the addons directory
3. Create a zip file for the Kuesa tools addons
 * zip -r kuesa.zip kuesa
4. Move into kuesa_exporter/glTF-Blender-Exporter/scripts/addons/
5. Create a zip file for the Kuesa exporter
 * cd kuesa_exporter/glTF-Blender-Exporter/scripts/addons/
 * zip -r kuesa_exporter.zip io_scene_gltf2
6. Launch Blender
7. Go to: Files -> User Preferences -> Add-ons -> Install Add-on from File...
8. Search and add each zip file (one at a time)
9. In the Add-ons search field, type kuesa
10. You should now see two entries:
 * All: KDAB - Kuesa Tool for Blender
 * Import-Exporter: KDAB Kuesa glTF format
11. Select them both and hit Save User Settings

Notes: you will have to repeat the process any time the repositories are updated.

### Instructions if you plan on modifying the addons

1. Clone the repository
2. Locate your Blender add-ons directory (e.g /usr/share/blender/2.79/scripts/addons/)
3. Copy (or link) addons/kuesa into your Blender add-ons directory
4. Copy (or link) addons/kuesa_exporter/glTF-Blender-Exporter/scripts/addons/io_scene_gltf2 into your Blender add-ons directory
5. Go to: Files -> User Preferences -> Add-ons -> Install Add-on from File...
6. In the Add-ons search field, type kuesa
7. You should now see two entries:
 * All: KDAB - Kuesa Tool for Blender
 * Import-Exporter: KDAB Kuesa glTF format
8. Select them both and hit Save User Settings

