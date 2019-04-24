
import unittest
import sys
import os

import_path = os.path.join(os.path.split(sys.argv[sys.argv.index("--")+1])[0], "scripts", "addons", "io_scene_gltf2")
print("import path:", import_path)
sys.path.append(import_path)

from kdab_fixquats import *

class TestLayerManager(unittest.TestCase):

    def test_caching(self):
        FixQuats.reset()
        self.assertTrue(FixQuats.len() == 0)
        FixQuats.get("n1", "a1");
        self.assertTrue(FixQuats.len() == 1)
        FixQuats.get("n1", "a1");
        self.assertTrue(FixQuats.len() == 1)
        FixQuats.get("n1", "a2");
        self.assertTrue(FixQuats.len() == 2)
        FixQuats.get("n1", "a1");
        self.assertTrue(FixQuats.len() == 2)
        FixQuats.get("n2", "a1");
        self.assertTrue(FixQuats.len() == 3)
        FixQuats.get("n1", "a1");
        self.assertTrue(FixQuats.len() == 3)
        FixQuats.debug()
        FixQuats.reset()
        self.assertTrue(FixQuats.len() == 0)

    def test_quats(self):
        FixQuats.reset()
        fq = FixQuats.get("n1", "a1");
        r = None
        for q in [
            mathutils.Quaternion([ 1.0,  0.9, 0.0, 0.0]),
            mathutils.Quaternion([ 1.0,  1.0, 0.0, 0.0]),
            mathutils.Quaternion([-1.0, -0.9, 0.0, 0.0]) ]:
            r = fq(q)
            print(r)
        self.assertTrue(cmpFloat(r.x, 0.9))

    def cmpFloat(a, b):
        d = a - b
        return d*d < 0.0001
