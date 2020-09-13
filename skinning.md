# Skinning

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
