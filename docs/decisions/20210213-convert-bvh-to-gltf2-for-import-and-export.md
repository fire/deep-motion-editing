# Convert BVH to GLTF2 for import and export

- Status: proposed <!-- optional -->
- Deciders: fire <!-- optional -->
- Date: 2021-02-13 <!-- optional. To customize the ordering without relying on Git creation dates and filenames -->
- Tags: data,pipeline,import <!-- optional -->

## Context and Problem Statement

How do we ingest data? Keep it proper and have compatible outputs.

## Decision Drivers <!-- optional -->

- Inconsistent up, front and scale
- Not standardized format

## Considered Options

- FBX
- BVH
- GLTF2

## Decision Outcome

GLTF2 is the only choice because FBX and BVH are not standardized formats. Not BVH or FBX because they do not standardize on up, front or scale.

### Positive Consequences <!-- optional -->

- Standardized import gives better data for learning
- Expect better gain
- Godot supports GLTF2

### Negative Consequences <!-- optional -->

- Requires blender tooling
- GLTF2 is not a standard format
- Needs a GLTF2 python library

## Pros and Cons of the Options <!-- optional -->

### FBX

FBX can be an interchange format.

- Good, because it is the most common
- Good, because it is already coded to work
- Bad, because FBX does not have a spec.

### BVH

BVH is a way to import and export animations.

- Good, because it already is here
- Good, because no extra code
- Bad, because there was great difficulty finding Euler order, up, scale and forward

### GLTF2

GLTF is a new open specification 3d interface format.

1. Ingest anything to a skeleton in Blender
1. Generate meshes for the bones
1. Export to glTF2.
1. Pick a python library that can read simple skin gltf2
1. Read gltf2
1. Input into ML PyTorch
1. process
1. Output into glTF2
1. Trash mesh and recreate meshes
1. Output glTF2

- Good, because it is a standard
- Good, because we don't have problems with 3d conventions
- Good, because I have experience with GLTF2 and less with the other formats.
- Bad, because python libraries to handle gltf2 may be underbaked
- Bad, because some work needs to be done

## Links <!-- optional -->

- … <!-- numbers of links can vary -->
