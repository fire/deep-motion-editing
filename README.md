# Deep-motion-editing

![Python](https://img.shields.io/badge/Python->=3.7-Blue?logo=python)  ![Pytorch](https://img.shields.io/badge/PyTorch->=1.5.0-Red?logo=pytorch)
![Blender](https://img.shields.io/badge/Blender-%3E=2.8-Orange?logo=blender)

This library provides fundamental and advanced functions to work with 3D character animation in deep learning with Pytorch. The code contains end-to-end modules, from reading and editing animation files to visualizing and rendering (using Blender) them.

The main deep editing operations provided here, motion retargeting and motion style transfer, are based on two works published in SIGGRAPH 2020:

**Skeleton-Aware Networks for Deep Motion Retargeting**: [Project](https://deepmotionediting.github.io/retargeting) | [Paper](https://arxiv.org/abs/2005.05732) |
[Video](https://www.youtube.com/watch?v=ym8Tnmiz5N8)

<img src="images/retargeting_teaser.gif" align="center"> <br>

**Unpaired Motion Style Transfer from Video to Animation**: [Project](https://deepmotionediting.github.io/style_transfer) | [Paper](https://arxiv.org/abs/2005.05751) |
[Video](https://www.youtube.com/watch?v=m04zuBSdGrc)

<img src="images/style_transfer_teaser.gif" align="center"> <br>


This library is written and maintained by [Kfir Aberman](https://kfiraberman.github.io), [Peizhuo Li](https://peizhuoli.github.io/) and [Yijia Weng](https://halfsummer11.github.io/). The library is still under development.

## Prerequisites

- Linux or macOS
- Python 3
- CPU or NVIDIA GPU + CUDA CuDNN

## Quick Start
We provide pretrained models together with demo examples using animation files specified in bvh format.

<!--```bash
python test.py -model_path MODEL_PATH -input_A PATH_A -input_B PATH_B -edit_type TYPE
```-->

### Motion Retargeting
<!-- `TYPE = retargeting`  
`PATH_A` - motion input  
`PATH_B` - skeleton input -->

Download and extract the test dataset from [Google Drive](https://docs.google.com/uc?export=download&id=1_849LvuT3WBEHktBT97P2oMBzeJz7-UP) or [Baidu Disk](https://pan.baidu.com/s/1z1cQiqLUgjfxlWoajIPr0g) (ye1q). Then place the `Mixamo` directory within `retargeting/datasets`.

To generate the demo examples with the pretrained model, run

```bash
cd retargeting
sh demo.sh
```

The results will be saved in `retargeting/examples`.

To reconstruct the quantitative result with the pretrained model, run

```bash
cd retargeting
python test.py
```

The retargeted demo results, that consists both intra-structual retargeting and cross-structural retargeting, will be saved in `retargeting/pretrained/results`.

<!-- The system support both in Intra-Structural retargeting:
```bash
python test.py -model_path retargeting/models/pretrained_retargeting.pth -input_A retargeting/examples/IS_motion_input -input_B retargeting/examples/IS_skeleton_input -edit_type retargeting
```
(demo result GIF: input_motion, input_skeleton, output)

and Cross-structural retargeting:
```bash
python test.py -model_path retargeting/models/pretrained_retargeting.pth -input_A retargeting/examples/CS_motion_input -input_B retargeting/examples/CS_skeleton_input -edit_type retargeting
```

(demo result GIF: input_motion, input_skeleton, output) -->

## Skinning

### Automatic Skinning

We provide a blender script that applies "skinning" to the output skeletons. You first need to download the fbx file which corresponds to the targeted character (for example, "[mousey](https://www.mixamo.com/#/?page=1&query=mousey&type=Character)"). Then, you can get a skinned animation by simply run

```sh
blender -P blender_rendering/skinning.py -- --bvh_file [bvh file path] --fbx_file [fbx file path]
```

Note that the script might not work well for all the fbx and bvh files. If it fails, you can try to tweak the script or follow the manual skinning guideline below.


### Manual Skinning

Here we provide a "quick and dirty" guideline for how to apply skin to the resulting bvh files, with blender:

- Download the fbx file that corresponds to the retargeted character (for example, "[mousey](https://www.mixamo.com/#/?page=1&query=mousey&type=Character)")
- Import the fbx file to blender (uncheck the "import animation" option)
- Merge meshes - select all the parts and merge them (ctrl+J)
- Import the retargeted bvh file
- Click "context" (menu bar) -> "Rest Position" (under sekeleton)
- Manually align the mesh and the skeleton (rotation + translation)
- Select the skeleton and the mesh (the skeleton object should be highlighted)
- Click Object -> Parent -> with automatic weights (or Ctrl+P)

Now the skeleton and the skin are bound and the animation can be rendered.


## Acknowledgments
The code in the utils directory is mostly taken from [Holden et al. [2016]](http://theorangeduck.com/page/deep-learning-framework-character-motion-synthesis-and-editing).  
In addition, part of the MoCap dataset is taken from [Adobe Mixamo](https://www.mixamo.com/) and from the work of [Xia et al.](http://faculty.cs.tamu.edu/jchai/projects/SIG15/style-final.pdf).

## Citation
If you use this code for your research, please cite our papers:
```bibtex
@article{aberman2020skeleton,
  author = {Aberman, Kfir and Li, Peizhuo and Sorkine-Hornung Olga and Lischinski, Dani and Cohen-Or, Daniel and Chen, Baoquan},
  title = {Skeleton-Aware Networks for Deep Motion Retargeting},
  journal = {ACM Transactions on Graphics (TOG)},
  volume = {39},
  number = {4},
  pages = {62},
  year = {2020},
  publisher = {ACM}
}
```
and
```bibtex
@article{aberman2020unpaired,
  author = {Aberman, Kfir and Weng, Yijia and Lischinski, Dani and Cohen-Or, Daniel and Chen, Baoquan},
  title = {Unpaired Motion Style Transfer from Video to Animation},
  journal = {ACM Transactions on Graphics (TOG)},
  volume = {39},
  number = {4},
  pages = {64},
  year = {2020},
  publisher = {ACM}
}
```
