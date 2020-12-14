import os
from posixpath import join as pjoin
from shutil import copyfile

import torch

import option_parser
from datasets import create_dataset
from models import create_model

def main():
    parser = option_parser.get_parser()
    parser.add_argument("--input_bvh", type=str, required=True)
    parser.add_argument("--target_bvh", type=str, required=False)
    parser.add_argument("--output_filename", type=str, required=True)
    parser.add_argument("--cpu", type=bool, required=False)
 
    args = parser.parse_args()
    
    input_bvh = args.input_bvh
    target_bvh = args.target_bvh
    cpu = args.cpu
  
    src_character = input_bvh.split("/")[-2]
    target_character = target_bvh.split("/")[-2]
    character_names = [[src_character], [target_character]]
    file_id = [[input_bvh], [target_bvh]]
    src_id = 0

    output_filename = args.output_filename

    test_device = args.cuda_device
    eval_seq = args.eval_seq
    
    para_path = pjoin(args.save_dir, "para.txt")
    with open(para_path, "r") as para_file:
        argv_ = para_file.readline().split()[1:]
        args = option_parser.get_parser().parse_args(argv_)

    args.cuda_device = test_device if torch.cuda.is_available() else "cpu"    
    if cpu:
        args.cuda_device = "cpu"
    print(f'Cuda device is {args.cuda_device}')
    args.is_train = False
    args.rotation = "quaternion"
    args.eval_seq = eval_seq

    dataset = create_dataset(args, character_names)
    model = create_model(args, character_names, dataset)
    model.load(epoch=0)
    input_motion = []

    if not os.path.exists(input_bvh):
        error = f'Cannot find file {input_bvh}'
        print(error)
        return

    input_motion = []
    for i, character_group in enumerate(character_names):
        input_group = []
        for j in range(len(character_group)):
            new_motion = dataset.get_item_string(file_id[i][j])
            new_motion.unsqueeze_(0)
            new_motion = (new_motion - dataset.mean[i][j]) / dataset.var[i][j]
            input_group.append(new_motion)
        input_group = torch.cat(input_group, dim=0)
        input_motion.append([input_group, list(range(len(character_group)))])

    model.set_input(input_motion)
    model.test()
    bvh_path = f"{model.bvh_path}/{target_character}/0_{src_id}.bvh"
    copyfile(bvh_path, output_filename)


if __name__ == "__main__":
    main()
