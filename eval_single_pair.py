import os
from posixpath import join as pjoin
from shutil import copyfile

import torch

import option_parser
from datasets import create_dataset
from models import create_model
from datasets import create_dataset, get_character_names, get_train_list, character_dict_to_list, train_dict


def main():
    parser = option_parser.get_parser()
    parser.add_argument("--input_bvh", type=str, required=True)
    parser.add_argument("--target_bvh", type=str, required=False)
    parser.add_argument("--output_filename", type=str, required=True)
    parser.add_argument("--cpu", type=bool, required=False)
    parser.add_argument("--convert_type", type=str, required=True)

    args = parser.parse_args()

    input_bvh = args.input_bvh
    target_bvh = args.target_bvh
    cpu = args.cpu
    _convert_type = args.convert_type

    src_character = input_bvh.split("/")[-2]
    target_character = target_bvh.split("/")[-2]
    print(f'Source character {src_character}')
    print(f'Target character {target_character}')
    character_names = []
    file_id = []
    topo_index = -1
    topologies = character_dict_to_list(train_dict)
    for t, topo in enumerate(topologies):
        print(f'Topologies are {topo}')
        if src_character in topo[1] and target_character in topo[0]:
            topo_index = t
            break
    
    if topo_index % 2 == 0:    
        character_names.append([target_character])
        file_id.append([target_bvh])
        character_names.append([src_character])
        file_id.append([input_bvh])
    else:
        character_names.append([src_character])
        file_id.append([input_bvh])
        character_names.append([target_character])
        file_id.append([target_bvh])

    character_names = [character_names]
    print(f'Character names {character_names}')
    print(f'File id {file_id}')
    print(f'Topo index {topo_index}')

    output_filename = args.output_filename

    test_device = args.cuda_device

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
    print(f'Characters {character_names}')
    dataset = create_dataset(args, character_names)
    model = create_model(args, character_names, dataset, topologies)
    model.load(epoch=50, topology=topo_index)
    input_motion = []

    if not os.path.exists(input_bvh):
        error = f'Cannot find file {input_bvh}'
        print(error)
        return

    input_motion = []
    for i in range(2):
        input_group = []
        new_motion = dataset.get_item(file_id[i][0])
        new_motion.unsqueeze_(0)
        new_motion = (new_motion - dataset.mean[i][0]) / dataset.var[i][0]
        input_group.append(new_motion) 
        input_group = torch.cat(input_group, dim=0)
        input_motion.append([input_group, list(range(1))])    
    model.set_input(input_motion)
    model.test()
    # ---- Output 
    bvh_path = f"{model.bvh_path}/{topologies[topo_index][1][0]}/0_{topo_index}.bvh"
    print(f'BVH path {bvh_path}')
    copyfile(bvh_path, output_filename)


if __name__ == "__main__":
    main()
