import os
from posixpath import join as pjoin
from shutil import copyfile

import torch

import option_parser
from datasets import create_dataset
from models import create_model
from datasets import create_dataset, get_character_names, get_train_list


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
    print(f'Source character {src_character}')
    print(f'Target character {target_character}')
    character_names = []
    file_id = []
    topo_index = -1
    final_character = ""
    topologies = get_character_names(args)
    print(f'Topologies are {topologies}')
    for n, names in enumerate(topologies):
        if src_character in names[1] and target_character in names[0]:
            character_names.append([target_character])
            file_id.append([target_bvh])
            character_names.append([src_character])
            file_id.append([input_bvh])
            final_character = target_character
            topo_index = n
            break

    print(character_names)
    print(file_id)
    print(topo_index)

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

    dataset = create_dataset(args, [character_names])
    model = create_model(args, [character_names], dataset, get_train_list())
    model.load(epoch=5000, topology=topo_index)
    input_motion = []

    if not os.path.exists(input_bvh):
        error = f'Cannot find file {input_bvh}'
        print(error)
        return

    input_motion = []
    for i, character_group in enumerate(character_names):
        input_group = []
        for j in range(len(character_group)):
            group_anim = file_id[i][j]
            print(f'Group anim is {group_anim}')
            new_motion = dataset.get_item_string(group_anim)
            new_motion.unsqueeze_(0)
            new_motion = (new_motion - dataset.mean[i][j]) / dataset.var[i][j]
            input_group.append(new_motion)
        input_group = torch.cat(input_group, dim=0)
        input_motion.append([input_group, list(range(len(character_group)))])
        model.set_input(input_motion)
        model.test()
    bvh_path = f"{model.bvh_path}/{final_character}/{topo_index}_0.bvh"
    copyfile(bvh_path, output_filename)


if __name__ == "__main__":
    main()
