# Deep-motion-targeting

This library provides fundamental and advanced functions to work with 3D character animation in deep learning with Pytorch.

This library is maintained by [K. S. Ernest (iFire) Lee](https://github.com/fire).

The main deep editing operations provided here, motion retargeting, are based on work published in SIGGRAPH 2020:

This library was written by [Kfir Aberman](https://kfiraberman.github.io), [Peizhuo Li](https://peizhuoli.github.io/) and [Yijia Weng](https://halfsummer11.github.io/).

**Skeleton-Aware Networks for Deep Motion Retargeting**: [Project](https://deepmotionediting.github.io/retargeting) | [Paper](https://arxiv.org/abs/2005.05732) |
[Video](https://www.youtube.com/watch?v=ym8Tnmiz5N8)

## Prerequisites

* Linux or macOS
* Python 3
* CPU or NVIDIA GPU + CUDA CuDNN

Retarget one animation.

### Motion Retargeting

Download and extract the test dataset from https://github.com/fire/deep-motion-editing/releases/download/v0.1-alpha/training_set.tar.bz2. Then place the `Mixamo` directory within `datasets` .

To generate the demo examples with the pretrained model, run

```bash
python3 demo
```

The results will be saved in `examples` .

To reconstruct the quantitative result with the pretrained model, run

``` bash
python3 test
```

The retargeted demo results, that consists both intra-structual retargeting and cross-structural retargeting, will be saved in `pretrained/results` .

## Train from scratch

We provide instructions for retraining our models

### Motion Retargeting

#### Dataset

* `scoop install miniconda3` Install miniconda.

* Install cuda. `conda install -y pytorch torchvision torchaudio cudatoolkit=11.0 -c pytorch -c=conda-forge`

* Enter `datasets` directory and run `blender -b -P fbx2bvh.py` to convert fbx files to bvh files. If you already have bvh file as dataset, please skip this step.

* Run `python datasets/preprocess.py` to simplify the skeleton by removing some less interesting joints, e.g. fingers and convert bvh files into npy files. If you use your own data, you'll need to define simplified structure in `datasets/bvh_parser.py` . This information currently is hard-coded in the code. See the comment in source file for more details. There are four steps to make your own dataset work.

* Training and testing character are hard-coded in `datasets/__init__.py` . You'll need to modify it if you want to use your own dataset.

#### Train

After preparing dataset, simply run 

``` bash
python3 train --save_dir=./training/
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
