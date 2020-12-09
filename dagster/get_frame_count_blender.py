import sys
import bpy

argv = sys.argv
argv = argv[argv.index("--") + 1:]
path = argv[0]
bpy.ops.import_scene.gltf(filepath=f'{path}')


output = {}

output["first_keyframe"] = 0
output["last_keyframe"] = 0

# https://blender.stackexchange.com/a/27946
if bpy.data.actions:
    # get all actions
    action_list = [action.frame_range for action in bpy.data.actions]

    # sort, remove doubles and create a set
    keys = (sorted(set([item for sublist in action_list for item in sublist])))

    # print first and last keyframe
    output["first_keyframe"] = keys[0]
    output["last_keyframe"] = keys[-1]

import json

json_object = json.dumps(output, ensure_ascii=False, indent = 4)   

f = open(f'{path}.json', 'wb')
f.write(bytes(json_object, encoding='utf8'))
f.close() 