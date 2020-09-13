# Usage

#### Arguments

Due to blender's argparse system, the argument list should be separated from the python file with an extra '--', for example:

 `blender -P render.py -- --arg1 [ARG1] --arg2 [ARG2]`
engine: "cycles" or "eevee". Please refer to `Render` section for more details.

render: 0 or 1. If set to 1, the data will be rendered outside blender's GUI. It is recommended to use render = 0 in case you need to manually adjust the camera.

The full parameters list can be displayed by:
 `blender -P render.py -- -h`

#### Load bvh File ( `load_bvh.py` )

To load `example.bvh` , run `blender -P load_bvh.py` . Please finish the preparation first.

> Note that currently it uses primitive_cone with 5 vertices for limbs.

> Note that Blender and bvh file have different xyz-coordinate systems. In bvh file, the "height" axis is y-axis while in blender it's z-axis. `load_bvh.py` swaps the axis in the `BVH_file` class initialization funtion.

> Currently all the `End Sites` in bvh file are discarded, this is because of the out-side code used in `utils/` .

> After loading the bvh file, it's height is normalized to 10.

#### Material, Texture, Light and Camera (`scene.py`)

This file enables to add a checkerboard floor, camera, a "sun" to the scene and to apply a basic color material to character.

The floor is placed at y=0, and should be corrected manually in case that it is needed (depends on the character parametes in the bvh file).

## Rendering

We support 2 render engines provided in Blender 2.80: Eevee and Cycles, where the trade-off is between speed and quality.

Eevee (left) is a fast, real-time, render engine provides limited quality, while Cycles (right) is a slower, unbiased, ray-tracing render engine provides photo-level rendering result. Cycles also supports CUDA and OpenGL acceleration.

<p float="left">
  <img src="images/eevee.png" width="300" />
  <img src="images/cycles.png" width="300" />
</p>

## Skinning

### Automatic Skinning

We provide a blender script that applies "skinning" to the output skeletons. You first need to download the fbx file which corresponds to the targeted character (for example, "[mousey](https://www.mixamo.com/#/?page=1&query=mousey&type=Character)"). Then, you can get a skinned animation by simply run

``` sh
blender -P blender_rendering/skinning.py -- --bvh_file [bvh file path] --fbx_file [fbx file path]
```

Note that the script might not work well for all the fbx and bvh files. If it fails, you can try to tweak the script or follow the manual skinning guideline below.

### Manual Skinning

Here we provide a "quick and dirty" guideline for how to apply skin to the resulting bvh files, with blender:

* Download the fbx file that corresponds to the retargeted character (for example, "[mousey](https://www.mixamo.com/#/?page=1&query=mousey&type=Character)")
* Import the fbx file to blender (uncheck the "import animation" option)
* Merge meshes - select all the parts and merge them (ctrl+J)
* Import the retargeted bvh file
* Click "context" (menu bar) -> "Rest Position" (under sekeleton)
* Manually align the mesh and the skeleton (rotation + translation)
* Select the skeleton and the mesh (the skeleton object should be highlighted)
* Click Object -> Parent -> with automatic weights (or Ctrl+P)

Now the skeleton and the skin are bound and the animation can be rendered.
