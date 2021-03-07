train_dict = {
    "corps_name_1": ["mixamo_tpose_1",],
    "corps_number_1": ["godot_girl_1",],
}
test_dict = train_dict


def get_character_names(args):
    characters = {}
    if args.is_train:
        """
        Put the name of subdirectory in retargeting/datasets/Mixamo as [[names of group A], [names of group B]]
        """
        characters = train_dict
    else:
        """
        To run evaluation successfully, number of characters in both groups must be the same. Repeat is okay.
        """
        characters = test_dict

    return character_dict_to_list(characters)


import itertools as it


def character_dict_to_list(chars: dict):
    topo = []
    for key in chars.values():
        topo.append(key)
    topo = [list(x) for x in it.permutations(topo, 2)]
    return topo


def create_dataset(args, character_names=None):
    from datasets.combined_motion import TestData, MixedData

    if args.is_train:
        return MixedData(args, character_names, get_character_names(args))
    else:
        return TestData(args, character_names, get_character_names(args))


def get_test_list():
    test_list = []
    for keys in test_dict.values():
        for k in keys:
            test_list.append(k)
    return test_list


def get_train_list():
    train_list = []
    for keys in train_dict.values():
        for k in keys:
            train_list.append(k)
    return train_list
