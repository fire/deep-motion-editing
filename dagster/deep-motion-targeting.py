from dagster import execute_pipeline, pipeline, solid
import requests

#########################################

# @solid
# Train motion targeting model

# @solid
# rename mixamo rig names to vrm

@solid
def base_row_table_api_jwt(_):
    return ""

@solid
def one(_):
    return 1

@solid
def fetch_vrm_metadata(_, api_jwt: str, page: int):
    url =  f"https://api.baserow.io/api/database/rows/table/5785/?size={str(page)}&page=1"
    req = requests.get(
        url,
        headers={
            "Authorization": f"Token {api_jwt}" 
        }
    )
    return req.text

import json as j
@solid
def fetch_vrm_gltf(context, json: str):
    doc = j.loads(json) 
    for d in doc:   
        context.log.info(d)

# @solid 
# normalize each bvh to be
# * y up 
# * z forward
# Use bounding box and location of the stick figure bones
# hands
# head
# feet

# @solid
# for each vrm in folder


# @solid
# convert a vrm binary string 
# store binary into a PandasColumn

# @solid
# open vrm in blender
# Cond does vrm have animations?


# @solid
# add animations to the vrm
# See prior work at maya gltf exporter


# @solid
# check if the vrm is within the volume of a normal person


# @solid
# Dictionary of original rig to vrm names
# rename known rigs to vrm bone names


# @solid
# enforce t-pose


# @solid
# ? remove fingers


# @solid
# ? split skeleton spine bones


# @solid 
# convert to bvh


# @solid
# Take original vrm and put the animation on it.
# Does vrm allow animations?


# @solid
# input 1
# A) list of known and taught bvh animation as a source 
# B) trained ml model (ml metadata)
# C) Orientation of the bvh forward and up axis -> gltf metadata
# input 2
# use the incoming untrained bvh

@pipeline
def deep_motion_targeting():
    i = one()
    api_jwt = base_row_table_api_jwt()
    n = fetch_vrm_metadata(api_jwt, i)
    fetch_vrm_gltf(n)