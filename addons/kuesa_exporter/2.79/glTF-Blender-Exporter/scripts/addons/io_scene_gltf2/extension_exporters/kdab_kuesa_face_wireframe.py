from bpy.props import BoolProperty

class KDABKuesaFaceWireframe:
    ext_meta = {
        'name': 'KDAB_Kuesa_FaceWireframe',
        'isDraft': False,
        'enable': True,
        'url': (
            'https://www.kdab.com'
        ),
        'settings': {
            'export_face_wireframe': BoolProperty(
                name='Export as Face Wireframe',
                description='Export geometry as per face lines instead of triangles',
                default=False
            )
        },
    }

    KDAB_kuesa_extension_name = 'KDAB_Kuesa_FaceWireframe'

    def export(self, export_settings, glTF):
        # Mark extension as being used
        glTF['extensionsUsed'] = glTF.get('extensionsUsed', [])
        glTF['extensionsUsed'].append(self.KDAB_kuesa_extension_name)
