# KineticTransfer-GAN

This library provides fundamental and advanced functions to work with 3D character animation in deep learning with Pytorch.

This library is maintained by [K. S. Ernest (iFire) Lee](https://github.com/fire).

## Prerequisites

* Windows 10, Linux or macOS
* Python 3
* CPU or NVIDIA GPU + CUDA CuDNN

Retarget one animation to another animation. 

Each animation must belong to a certain skeleton topology and each skeleton topology should have 9,000 frames of animation. The required frames per topology may be reduced but these frame requirements were the reported numbers.

### Motion Retargeting

The test dataset is included in the Motions directory within `datasets`.

To generate the demo examples with the pretrained model, run

```bash
python3 demo --save_dir=pretrained
```

The results will be saved in `examples` .

To reconstruct the quantitative result with the pretrained model, run

``` bash
python3 test
```

#### Dataset

* `scoop install miniconda3` Install miniconda.

* Install cuda. `conda install -y pytorch torchvision torchaudio cudatoolkit=11.0 -c pytorch -c=conda-forge`

* Enter `datasets` directory and run `blender -b -P fbx2bvh.py` or `blender -b -P gltf2bvh.py` to convert fbx files to bvh files. If you already have bvh file as dataset, please skip this step.

* Run `python datasets/preprocess.py` to simplify the skeleton by removing some less interesting joints, e.g. fingers and convert bvh files into npy files. If you use your own data, you'll need to define simplified structure in `datasets/bvh_parser.py` . This information currently is hard-coded in the code. See the comment in source file for more details. There are four steps to make your own dataset work.

* Training and testing character are hard-coded in `datasets/__init__.py` . You'll need to modify it if you want to use your own dataset.

#### Train

After preparing dataset, simply run 

``` bash
python3 train
```

It will use default hyper-parameters to train the model and save trained model in `training` directory. More options are available in `option_parser.py` . You can use tensorboard to monitor the training progress by running

``` bash
tensorboard --logdir=./training/logs/
```

## Train from scratch

We provide instructions for retraining our models.

## Acknowledgments

The code in the utils directory is mostly taken from [Holden et al. [2016]](http://theorangeduck.com/page/deep-learning-framework-character-motion-synthesis-and-editing).  

In addition, part of the MoCap dataset is taken from [Adobe Mixamo](https://www.mixamo.com/) and from the work of [Xia et al.](http://faculty.cs.tamu.edu/jchai/projects/SIG15/style-final.pdf), however these MoCap datasets have been removed from the git HEAD.

The main deep editing operations provided here, motion retargeting, are based on work published in SIGGRAPH 2020 by [Kfir Aberman](https://kfiraberman.github.io), [Peizhuo Li](https://peizhuoli.github.io/) and [Yijia Weng](https://halfsummer11.github.io/). Skeleton-Aware Networks for Deep Motion Retargeting: [Project](https://deepmotionediting.github.io/retargeting) | [Paper](https://arxiv.org/abs/2005.05732) |
[Video](https://www.youtube.com/watch?v=ym8Tnmiz5N8)

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
