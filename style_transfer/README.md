# Quick Start

We provide pretrained models together with demo examples using animation files specified in bvh format.

<!--

``` bash
python test.py -model_path MODEL_PATH -input_A PATH_A -input_B PATH_B -edit_type TYPE
```-->

### Motion Style Transfer

<!-- `TYPE = style_transfer`
`PATH_A` - content motion input  
`PATH_B` - style motion input  

The system support both in style from 3D MoCap data:

``` bash
python test.py -model_path retargeting/models/pretrained_style_transfer.pth -input_A style_transfer/examples/content_input -input_B style_transfer/examples/3D_style_input -edit_type style_transfer
```

(demo result GIF: input_content, input_style, output)

and in style from 2D key-points (extracted from video):

``` bash
python test.py -model_path retargeting/models/pretrained_style_transfer.pth -input_A style_transfer/examples/content_input -input_B style_transfer/examples/2D_style_input -edit_type style_transfer
```

(demo result GIF: input_content, input_style_video, output) -->
To receive the demo examples, simply run

``` bash
sh style_transfer/demo.sh
```

The results will be saved in `style_transfer/demo_results` , 
where each folder contains the raw output `raw.bvh` and the output after footskate clean-up `fixed.bvh` .

## Train from scratch

We provide instructions for retraining our models

### Motion Style Transfer

#### Dataset

* Download the dataset from [Google Drive](https://drive.google.com/drive/folders/1C-_iZJj-PSUWZwh25yAsQe1tLpPm9EZ5?usp=sharing) or [Baidu Drive](https://pan.baidu.com/s/1LtZaX7bQ6kz8TrDWd4FxWA) (zzck). The dataset consists of two parts: one is the taken from the motion style transfer dataset proposed by [Xia et al.](http://faculty.cs.tamu.edu/jchai/projects/SIG15/style-final.pdf) and the other is our BFA dataset, where both parts contain .bvh files retargeted to the standard skeleton of [CMU mocap dataset](http://mocap.cs.cmu.edu/).
* Extract the .zip files into `style_transfer/data`
* Pre-process data for training:

  

``` bash
  cd style_transfer/data_proc
  sh gen_dataset.sh
  ```

  This will produce `xia.npz` , `bfa.npz` in `style_transfer/data` .

#### Train

After downloading the dataset simply run

``` bash
python style_transfer/train.py
```

#### Style from videos

To run our models in test time with your own videos, you first need to use [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) to extract the 2D joint positions from the video, then use the resulting JSON files as described in the demo examples.
