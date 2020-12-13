import itertools as it

def get_character_names(args):
    group_a = [
        "BerkeleyMHAD_skl_s05",
        "BerkeleyMHAD_skl_s06",
        # "BerkeleyMHAD_skl_s07",
        # "BerkeleyMHAD_skl_s08",
        # "BerkeleyMHAD_skl_s01",
        # "BerkeleyMHAD_skl_s02",
        # "BerkeleyMHAD_skl_s03",
    ]
    # group_b = [
    #     "Female1",
    # ]
    group_c = [
        "BerkeleyMHAD_skl_s04", 
    ]
    characters = []

    if args.is_train:
        """
        Put the name of subdirectory in retargeting/datasets/Mixamo as [[names of group A], [names of group B]]
        """
        all_groups = [group_a, group_c]
        characters = [list(x) for x in it.permutations(all_groups, 2)]
        print(characters)

    else:
        """
        To run evaluation successfully, number of characters in both groups must be the same. Repeat is okay.
        """
        characters = [
            [
                "BerkeleyMHAD_skl_s09",
                "BerkeleyMHAD_skl_s10",
            ],
            [
                "BerkeleyMHAD_skl_s07",
                "BerkeleyMHAD_skl_s08",
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