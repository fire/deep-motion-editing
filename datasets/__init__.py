def get_character_names(args):
    group_a = [
        "Kaya",
    ]
    group_b = [
    ]
    group_c = [
        "Female1",
    ]
    group_d = [
        "BerkeleyMHAD_skl_s05",
        "BerkeleyMHAD_skl_s06",
        "BerkeleyMHAD_skl_s07",
        "BerkeleyMHAD_skl_s08",
        "BerkeleyMHAD_skl_s01",
        "BerkeleyMHAD_skl_s02",
        "BerkeleyMHAD_skl_s03",
        "BerkeleyMHAD_skl_s04", ]

    if args.is_train:
        """
        Put the name of subdirectory in retargeting/datasets/Mixamo as [[names of group A], [names of group B]]
        """
        characters = [
            group_d,
            group_a,
        ]

    else:
        """
        To run evaluation successfully, number of characters in both groups must be the same. Repeat is okay.
        """
        characters = [
            [
                "Kaya", "Kaya",
            ],
            [
                "BerkeleyMHAD_skl_s05", "BerkeleyMHAD_skl_s06"
            ],
        ]
        tmp = characters[1][args.eval_seq]
        characters[1][args.eval_seq] = characters[1][0]
        characters[1][0] = tmp

    return characters


def create_dataset(args, character_names=None):
    from datasets.combined_motion import TestData, MixedData

    if args.is_train:
        return MixedData(args, character_names)
    else:
        return TestData(args, character_names)


def get_test_set():
    open_test_list = []
    try:
        open_test_list = open("./datasets/Motions/test_list.txt", "r")
    except FileNotFoundError as e:
        return []
    with open_test_list as file:
        list = file.readlines()
        list = [f[:-1] for f in list]
        return list


def get_train_list():
    open_train_list = []
    try:
        open_train_list = open("./datasets/Motions/train_list.txt", "r")
    except FileNotFoundError as e:
        return []
    with open_train_list as file:
        list = file.readlines()
        list = [f[:-1] for f in list]
        return list
