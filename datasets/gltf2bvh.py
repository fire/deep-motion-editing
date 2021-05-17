"""
This code comes from https://github.com/rubenvillegas/cvpr2018nkn/blob/master/datasets/fbx2bvh.py
"""
from os import walk
import bpy
import numpy as np
import sys
from math import radians

sys.path.append(".")


data_path = "./Motions/"

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

                bpy.ops.wm.read_homefile(use_empty=True)

                bpy.ops.import_scene.gltf(filepath=sourcepath)

                # check if actions is empty
                if bpy.data.actions:

                    # get all actions
                    action_list = [action.frame_range for action in bpy.data.actions]

                    # sort, remove doubles and create a set
                    keys = (sorted(set([item for sublist in action_list for item in sublist])))

                    # print all keyframes
                    print (keys)

                    # print first and last keyframe
                    print ("{} {}".format("first keyframe:", keys[0]))
                    print ("{} {}".format("last keyframe:", keys[-1]))
                    frame_end = keys[-1]
                

                for i in range(len(bpy.context.scene.objects)):
                    element = bpy.context.scene.objects[i]
                    if element.type != "ARMATURE":
                        continue

                    bpy.context.view_layer.objects.active = element
                    element.select_set(state=True)
                    bpy.ops.export_anim.bvh(
                        filepath=dumppath,
                        frame_start= 1,
                        frame_end= frame_end,
                        root_transform_only=True,
                        rotate_mode="NATIVE",
                    )
                    bpy.data.actions.remove(bpy.data.actions[-1])

                    print(data_path + d + "/" + f + " processed.")
