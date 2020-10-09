import os
import torch
from models import create_model
from datasets import create_dataset
import option_parser
from shutil import copyfile
from posixpath import join as pjoin
import os
import sys
sys.path.append(".")
from datasets.bvh_parser import BVH_file
from datasets.bvh_writer import BVH_writer
from models.IK import fix_foot_contact

def eval_prepare(args):
    character = []
    file_id = []
    character_names = []
    character_names.append(args.input_bvh.split("/")[-2])
    character_names.append(args.target_bvh.split("/")[-2])
    if args.test_type == "intra":
        if character_names[0].endswith("_m"):
            character = [["BigVegas", "BigVegas"], character_names]
            file_id = [[0, 0], [args.input_bvh, args.input_bvh]]
            src_id = 1
        else:
            character = [character_names, ["Goblin_m", "Goblin_m"]]
            file_id = [[args.input_bvh, args.input_bvh], [0, 0]]
            src_id = 0
    elif args.test_type == "cross":
        if character_names[0].endswith("_m"):
            character = [[character_names[1]], [character_names[0]]]
            file_id = [[0], [args.input_bvh]]
            src_id = 1
        else:
            character = [[character_names[0]], [character_names[1]]]
            file_id = [[args.input_bvh], [0]]
            src_id = 0
    else:
        raise Exception("Unknown test type")
    return character, file_id, src_id


def recover_space(file):
    l = file.split("/")
    l[-1] = l[-1].replace("_", " ")
    return "/".join(l)


def main(input_file, ref_file, output_file_name, test_type):
    parser = option_parser.get_parser()
    parser.add_argument("--input_bvh", type=str, required=False)
    parser.add_argument("--target_bvh", type=str, required=False)
    parser.add_argument("--test_type", type=str, required=False)
    parser.add_argument("--output_filename", type=str, required=False)

    args = parser.parse_args()
    args.input_bvh = input_file
    args.target_bvh = ref_file
    args.output_filename = output_file_name
    args.test_type = test_type

    # argsparse can't take space character as part of the argument
    args.input_bvh = recover_space(args.input_bvh)
    args.target_bvh = recover_space(args.target_bvh)
    args.output_filename = recover_space(args.output_filename)

    character_names, file_id, src_id = eval_prepare(args)
    input_character_name = args.input_bvh.split("/")[-2]
    output_character_name = args.target_bvh.split("/")[-2]
    output_filename = args.output_filename

    test_device = args.cuda_device
    eval_seq = args.eval_seq

    para_path = pjoin(args.save_dir, "para.txt")
    with open(para_path, "r") as para_file:
        argv_ = para_file.readline().split()[1:]
        args = option_parser.get_parser().parse_args(argv_)

    args.cuda_device = test_device if torch.cuda.is_available() else "cpu"
    args.is_train = False
    args.rotation = "quaternion"
    args.eval_seq = eval_seq

    dataset = create_dataset(args, character_names)

    model = create_model(args, character_names, dataset)
    model.load(epoch=20000)

    input_motion = []
    for i, character_group in enumerate(character_names):
        input_group = []
        for j in range(len(character_group)):
            new_motion = dataset.get_item(i, j, file_id[i][j])
            new_motion.unsqueeze_(0)
            new_motion = (new_motion - dataset.mean[i][j]) / dataset.var[i][j]
            input_group.append(new_motion)
        input_group = torch.cat(input_group, dim=0)
        input_motion.append([input_group, list(range(len(character_group)))])

    model.set_input(input_motion)
    model.test()
    bvh_path = "{}/{}/0_{}.bvh".format(model.bvh_path, output_character_name, src_id)
    copyfile(bvh_path, output_filename)

    # TODO Random input
    traced_script_module = torch.jit.trace(model, input_motion)


# downsampling and remove redundant joints
def copy_ref_file(src, dst):
    file = BVH_file(src)
    writer = BVH_writer(file.edges, file.names)
    writer.write_raw(file.to_tensor(quater=True)[..., ::2], 'quaternion', dst)


def get_height(file):
    file = BVH_file(file)
    return file.get_height()


def example(src_name, dest_name, bvh_name, test_type, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    input_file = './datasets/Mixamo/{}/{}'.format(src_name, bvh_name)
    ref_file = './datasets/Mixamo/{}/{}'.format(dest_name, bvh_name)
    copy_ref_file(input_file, pjoin(output_path, 'input.bvh'))
    copy_ref_file(ref_file, pjoin(output_path, 'gt.bvh'))
    height = get_height(input_file)

    bvh_name = bvh_name.replace(' ', '_')
    input_file = './datasets/Mixamo/{}/{}'.format(src_name, bvh_name)
    ref_file = './datasets/Mixamo/{}/{}'.format(dest_name, bvh_name)

    main(input_file, ref_file, pjoin(output_path, 'result.bvh'), test_type)


if __name__ == '__main__':
    example('BigVegas', 'Mousey_m', 'Dual Weapon Combo.bvh', 'cross', './examples/cross_structure')
    print('Finished!')
