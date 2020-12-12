"""
This code comes from https://github.com/rubenvillegas/cvpr2018nkn/blob/master/datasets/fbx2bvh.py
"""
import bpy
import numpy as np
import sys
from math import radians

sys.path.append(".")

from os import walk

data_path = "./datasets/Motions/"

for _, dirs, _ in sorted([f for f in walk(data_path)]):
    for d in dirs:
        if d.startswith("."):
            continue
        for _, _, files in sorted([f for f in walk(data_path + d)]):
            for f in files:
                if not (f.endswith(".glb") or f.endswith(".gltf")):
                    continue
                sourcepath = data_path + d + "/" + f
                dumppath = data_path + d + "/" + f.split(".")[0] + ".bvh"

                bpy.ops.import_scene.gltf(filepath=sourcepath)
                
                frame_start = 9999
                frame_end = -9999
                action = bpy.data.actions[-1]
                if action.frame_range[1] > frame_end:
                    frame_end = action.frame_range[1]
                if action.frame_range[0] < frame_start:
                    frame_start = action.frame_range[0]

                frame_end = np.max([60, frame_end])
                                
                for i in range(len(bpy.context.scene.objects)):
                    element = bpy.context.scene.objects[i]
                    if element.type != "ARMATURE":
                        continue
                    bpy.context.view_layer.objects.active = element
                    element.select_set(state=True)
                    bpy.ops.export_anim.bvh(
                        filepath=dumppath,
                        frame_start=frame_start,
                        frame_end=frame_end,
                        root_transform_only=True,
                    )
                    bpy.data.actions.remove(bpy.data.actions[-1])

                    print(data_path + d + "/" + f + " processed.")
