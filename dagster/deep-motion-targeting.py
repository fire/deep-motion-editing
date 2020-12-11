import pathlib
import tempfile
import json
import typing
from copy import deepcopy
from typing import Any

from dagster import (
    Bool,
    Field,
    Int,
    PythonObjectDagsterType,
    String,
    composite_solid,
    execute_pipeline,
    pipeline,
    solid,
)
import requests

if typing.TYPE_CHECKING:
    DataFrame = list
else:
    DataFrame = PythonObjectDagsterType(list, name="DataFrame")  # type: Any


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
def fetch_vrm_gltf_baserow(context, m: str):
    doc = json.loads(m)
    for r in doc["results"]:
        context.log.info(f'Name: {r[VRM_TABLE_NAME]}')
        files = r[VRM_TABLE_FILES]
        for f in files:
            url = f["url"]
            context.log.debug(f'Url: {url}')
            vrm_binary = requests.get(url, allow_redirects=True)
            return vrm_binary.content


@solid
def fetch_vrm_gltf_url(context, url: str):
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
                    f"{current_abs_path}/lib/get_frame_count_blender.py", "--", f'{temp_path}'])
    f = open(f'{temp_path}.json', 'rb')
    out = json.load(f)
    frames = out["last_keyframe"] - out["first_keyframe"]
    context.log.debug(f'Frames: {frames}')
    if frames < 1:
        raise ValueError
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
                    f'{current_abs_path}/lib/get_scene_info_blender.py', '--', temp_path])
    f = open(f'{temp_path}.json', 'rb')
    context.log.debug(str(f))
    return f


@solid
def get_url(_):
    return "https://github.com/KhronosGroup/glTF-Sample-Models/raw/master/2.0/Fox/glTF-Binary/Fox.glb"


@solid
def convert_to_bvh(context, has_enough_frames: bool, vrm) -> DataFrame:
    current_abs_path = pathlib.Path().absolute()
    temp = tempfile.mkdtemp(prefix='convert_to_bvh_')
    path = 'convert_to_bvh.vrm'
    temp_path = f'{temp}/{path}'
    f = open(temp_path, 'wb')
    f.write(vrm)
    f.close()
    import subprocess
    subprocess.run(["blender",  "--background", "--python",
                    f"{current_abs_path}/lib/convert_to_bvh_blender.py", "--", temp_path])
    f = open(f'{temp_path}.bvh', 'rb')
    bvh_doc = str(f)
    bvh = [[bvh_doc]]
    return bvh


@solid
def check_human_volume(_):
    pass


@solid
def remove_fingers(_):
    pass


@solid
def split_skeleton_spine(_):
    pass


@solid
def put_bvh_on_vrm(_):
    pass


@solid
def target_model(_, model, rig_bvhs: DataFrame):
    pass


@solid
def train_target_model(_, model, rig_bvhs: DataFrame) -> DataFrame:
    pass


@solid
def return_true(_):
    return True


@solid
def rename_rig_bones_to_vrm(vrm_bones, rig_bvh, common_rigs):
    pass


@composite_solid
def deep_motion_targeting(m: String) -> DataFrame:
    content = fetch_vrm_gltf_baserow(m)
    has_frames = check_num_of_vrm_frames(content)
    get_scene_info_of_vrm(content)
    bvh = convert_to_bvh(has_frames, content)
    return bvh


@composite_solid
def fetch_vrm() -> DataFrame:
    i = item()
    api_jwt = base_row_table_api_jwt()
    meta = fetch_vrm_metadata(api_jwt, i)
    return deep_motion_targeting(meta)


@pipeline
def target_motion():
    # result = fetch_vrm()
    content = fetch_vrm_gltf_url(get_url())
    # has_frames = check_num_of_vrm_frames(content)
    # get_scene_info_of_vrm(content)
    convert_to_bvh(return_true(), content)
