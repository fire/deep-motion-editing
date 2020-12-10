import pathlib
import tempfile
import json
import json as j
from dagster import execute_pipeline, pipeline, solid
import requests


@solid
def base_row_table_api_jwt(_):
    return "X2MGi5f82sirNY400ozVdpcMXLmiEqF9"


@solid
def item(_):
    return 2


@solid
def fetch_vrm_metadata(_, api_jwt: str, page: int):
    url = f"https://api.baserow.io/api/database/rows/table/5785/?size=1&page={str(page)}"
    req = requests.get(
        url,
        headers={
            "Authorization": f"Token {api_jwt}"
        }
    )
    return req.text


VRM_TABLE_NAME: str = "field_24361"
VRM_TABLE_FILES: str = "field_24364"


@solid
def fetch_vrm_gltf(context, json: str):
    doc = j.loads(json)
    for r in doc["results"]:
        context.log.info(f'Name: {r[VRM_TABLE_NAME]}')
        files = r[VRM_TABLE_FILES]
        for f in files:
            url = f["url"]
            context.log.debug(f'Url: {url}')
            vrm_binary = requests.get(url, allow_redirects=True)
            return vrm_binary.content


@solid
def check_num_of_vrm_frames(context, vrm) -> bool:
    current_abs_path = pathlib.Path().absolute()
    temp = tempfile.mkdtemp(prefix='check_num_of_vrm_frames_')
    path = 'check_num_of_vrm_frames.vrm'
    temp_path = f'{temp}/{path}'
    f = open(temp_path, 'wb')
    f.write(vrm)
    f.close()
    import subprocess
    subprocess.run(["blender", "--background", "--python",
                    f"{current_abs_path}/get_frame_count_blender.py", "--", f'{temp_path}'])
    f = open(f'{temp_path}.json', 'rb')
    context.log.debug(str(f))
    out = json.load(f)
    if out["last_keyframe"] - out["first_keyframe"] < 64:
        return False
    return True


@solid
def get_scene_info_of_vrm(context, vrm):
    current_abs_path = pathlib.Path().absolute()
    temp = tempfile.mkdtemp(prefix='get_scene_info_of_vrm_')
    path = 'get_scene_info_of_vrm.vrm'
    temp_path = f'{temp}/{path}'
    context.log.debug(f'Temporary file: {temp_path}')
    f = open(temp_path, 'wb')
    f.write(vrm)
    f.close()
    import subprocess
    subprocess.run(["blender", "--background", "--python",
                    f'{current_abs_path}/get_scene_info_blender.py', '--', temp_path])
    f = open(f'{temp_path}.json', 'rb')
    context.log.debug(str(f))
    return f


@solid
def convert_to_bvh(context, has_enough_frames: bool, vrm):
    if not has_enough_frames:
        raise ValueError
    current_abs_path = pathlib.Path().absolute()
    temp = tempfile.mkdtemp(prefix='convert_to_bvh_')
    path = 'convert_to_bvh.vrm'
    temp_path = f'{temp}/{path}'
    f = open(temp_path, 'wb')
    f.write(vrm)
    f.close()
    import subprocess
    subprocess.run(["blender",  "--background", "--python",
                    f"{current_abs_path}/convert_to_bvh_blender.py", "--", temp_path])
    f = open(f'{temp_path}.bvh', 'rb')
    char_count = f'Character count of bvh file: {len(str(f))}'
    context.log.debug(char_count)


# @solid
# get bvh of existing animation


# @solid
# normalize each bvh to be
# * y up
# * z forward
# Use bounding box of the skeleton
# hips and chest for the foward

# @solid
# check if the vrm is within the volume of a normal person


# @solid
# Dictionary of original rig to vrm names
# rename known rigs to vrm bone names


# @solid
# ? remove fingers


# @solid
# ? split skeleton spine bones


# @solid
# Take original vrm and put the animation on it.
# Does vrm allow animations?


# @solid
# input 1
# A) list of known and taught bvh animation as a source
# B) trained ml model (ml metadata)
# Assume gltf and its up and foward conventions
# input 2
# use the incoming untrained bvh

# @solid
# add animations to the vrm for preview

#########################################

# @solid
# Train motion targeting model

# @solid
# rename mixamo rig names to vrm


@pipeline
def deep_motion_targeting():
    i = item()
    api_jwt = base_row_table_api_jwt()
    n = fetch_vrm_metadata(api_jwt, i)
    content = fetch_vrm_gltf(n)
    has_frames = check_num_of_vrm_frames(content)
    get_scene_info_of_vrm(content)
    convert_to_bvh(has_frames, content)
