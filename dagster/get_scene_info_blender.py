import sys
import bpy

argv = sys.argv
argv = argv[argv.index("--") + 1:]
path = argv[0]
bpy.ops.import_scene.gltf(filepath=f'{path}')
list_of_meshes = []
# https://blender.stackexchange.com/questions/13757/list-of-objects-in-scene-with-counts-verts-faces-tris
for element in bpy.context.scene.objects:
    if element.type != "MESH": 
        continue
    output = {}
    output["name"] = element.data.name
    output["vertices"] = len(element.data.vertices)
    output["edges"] = len(element.data.polygons)
    print(str(output))
    list_of_meshes.append(output)

import json

json_object = json.dumps(list_of_meshes, ensure_ascii=False, indent = 4)   

f = open(f'{path}.json', 'wb')
f.write(bytes(json_object, encoding='utf8'))
f.close() 