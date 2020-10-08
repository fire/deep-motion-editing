# Deep-motion-editing

![Python](https://img.shields.io/badge/Python->=3.7-Blue?logo=python)  ![Pytorch](https://img.shields.io/badge/PyTorch->=1.5.0-Red?logo=pytorch)

![Blender](https://img.shields.io/badge/Blender-%3E=2.8-Orange?logo=blender)

This library provides fundamental and advanced functions to work with 3D character animation in deep learning with Pytorch. The code contains end-to-end modules, from reading and editing animation files to visualizing and rendering (using Blender) them.

The main deep editing operations provided here, motion retargeting, are based on work published in SIGGRAPH 2020:

**Skeleton-Aware Networks for Deep Motion Retargeting**: [Project](https://deepmotionediting.github.io/retargeting) | [Paper](https://arxiv.org/abs/2005.05732) |
[Video](https://www.youtube.com/watch?v=ym8Tnmiz5N8)

This library is written and maintained by [Kfir Aberman](https://kfiraberman.github.io), [Peizhuo Li](https://peizhuoli.github.io/) and [Yijia Weng](https://halfsummer11.github.io/). The library is still under development.

## Prerequisites

* Linux or macOS
* Python 3
* CPU or NVIDIA GPU + CUDA CuDNN

Retarget one animation.

```
python .\datasets\preprocess.py
python train.py --save_dir=./training/
python demo.py

``` 

### Motion Retargeting

Download and extract the test dataset from [Google Drive](https://docs.google.com/uc?export=download&id=1_849LvuT3WBEHktBT97P2oMBzeJz7-UP). Then place the `Mixamo` directory within `datasets` .

To generate the demo examples with the pretrained model, run

```bash
./demo
```

The results will be saved in `examples` .

To reconstruct the quantitative result with the pretrained model, run

``` bash
./test
```

The retargeted demo results, that consists both intra-structual retargeting and cross-structural retargeting, will be saved in `pretrained/results` .

## Train from scratch

We provide instructions for retraining our models

### Motion Retargeting

#### Dataset

We use Mixamo dataset to train our model. You can download our preprocessed data from [Google Drive](https://drive.google.com/file/d/1BYH2t5XMGWwnu5coftehU0rTXupQvFLg/view?usp=sharing). Then place the `Mixamo` directory within `datasets` .

Otherwise, if you want to download Mixamo dataset or use your own dataset, please follow the instructions below.

* To download Mixamo on your own, you can refer to [this](https://github.com/ChrisWu1997/2D-Motion-Retargeting/blob/master/dataset/Guide%20For%20Downloading%20Mixamo%20Data.md) good tutorial. You will need to download as fbx file (skin is not required) and make a subdirectory for each character in `datasets/Mixamo` . In our original implementation we download 60fps fbx files and downsample them into 30fps. Since we use an unpaired way in training, it is recommended to divide all motions into two equal size sets for each group and equal size sets for each character in each group. If you use your own data, you need to make sure that your dataset consists of bvh files with same t-pose. You should also put your dataset in subdirectories of `datasets/Mixamo` .

* Enter `datasets` directory and run `blender -b -P fbx2bvh.py` to convert fbx files to bvh files. If you already have bvh file as dataset, please skil this step.

* In our original implementation, we manually split three joints for skeletons in `group A` . If you want to follow our routine, run `python datasets/split_joint.py` . This step is optional.

* Run `python datasets/preprocess.py` to simplify the skeleton by removing some less interesting joints, e.g. fingers and convert bvh files into npy files. If you use your own data, you'll need to define simplified structure in `datasets/bvh_parser.py` . This information currently is hard-coded in the code. See the comment in source file for more details. There are four steps to make your own dataset work.

* Training and testing character are hard-coded in `datasets/__init__.py` . You'll need to modify it if you want to use your own dataset.

#### Train

After preparing dataset, simply run 

``` bash
python train.py --save_dir=./training/
```

It will use default hyper-parameters to train the model and save trained model in `training` directory. More options are available in `option_parser.py` . You can use tensorboard to monitor the training progress by running

``` bash
tensorboard --logdir=./training/logs/
```

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