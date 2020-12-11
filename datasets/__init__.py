def get_character_names(args):
    if args.is_train:
        """
        Put the name of subdirectory in retargeting/datasets/Mixamo as [[names of group A], [names of group B]]
        """
        characters = [
            ["Alicia_m"],
            [   "BerkeleyMHAD_skl_s01", 
                "BerkeleyMHAD_skl_s02", 
                "BerkeleyMHAD_skl_s03", 
                "BerkeleyMHAD_skl_s04",
                "BerkeleyMHAD_skl_s05",
                "BerkeleyMHAD_skl_s06",
                "BerkeleyMHAD_skl_s07",
                "BerkeleyMHAD_skl_s08",
            ],
        ]

    else:
        """
        To run evaluation successfully, number of characters in both groups must be the same. Repeat is okay.
        """
        characters = [
            ["Alicia", "Alicia", "Alicia", "Alicia",],
            ["BerkeleyMHAD_skl_s09", "BerkeleyMHAD_skl_s10", "BerkeleyMHAD_skl_s11", "BerkeleyMHAD_skl_s12"],
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
    with open("./datasets/Motions/test_list.txt", "r") as file:
        list = file.readlines()
        list = [f[:-1] for f in list]
        return list


def get_train_list():
    with open("./datasets/Motions/train_list.txt", "r") as file:
        list = file.readlines()
        list = [f[:-1] for f in list]
        return list
