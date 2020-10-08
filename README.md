# Deep-motion-editing

![Python](https://img.shields.io/badge/Python->=3.7-Blue?logo=python)  ![Pytorch](https://img.shields.io/badge/PyTorch->=1.5.0-Red?logo=pytorch)

![Blender](https://img.shields.io/badge/Blender-%3E=2.8-Orange?logo=blender)

This library provides fundamental and advanced functions to work with 3D character animation in deep learning with Pytorch. The code contains end-to-end modules, from reading and editing animation files to visualizing and rendering (using Blender) them.

The main deep editing operations provided here, motion retargeting, are based on work published in SIGGRAPH 2020:

**Skeleton-Aware Networks for Deep Motion Retargeting**: [Project](https://deepmotionediting.github.io/retargeting) | [Paper](https://arxiv.org/abs/2005.05732) |
[Video](https://www.youtube.com/watch?v=ym8Tnmiz5N8)

<img src="images/retargeting_teaser.gif" align="center"> <br>

This library is written and maintained by [Kfir Aberman](https://kfiraberman.github.io), [Peizhuo Li](https://peizhuoli.github.io/) and [Yijia Weng](https://halfsummer11.github.io/). The library is still under development.

## Prerequisites

* Linux or macOS
* Python 3
* CPU or NVIDIA GPU + CUDA CuDNN

## Acknowledgments

The code in the utils directory is mostly taken from [Holden et al. [2016]](http://theorangeduck.com/page/deep-learning-framework-character-motion-synthesis-and-editing).  
In addition, part of the MoCap dataset is taken from [Adobe Mixamo](https://www.mixamo.com/) and from the work of [Xia et al.](http://faculty.cs.tamu.edu/jchai/projects/SIG15/style-final.pdf).

## Citation

If you use this code for your research, please cite our papers:

``` bibtex
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