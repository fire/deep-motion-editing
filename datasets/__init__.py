train_set = {
    "corps_BerkeleyMHAD_01": [
        "BerkeleyMHAD_skl_s01",
        "BerkeleyMHAD_skl_s02",
        "BerkeleyMHAD_skl_s03",
        "BerkeleyMHAD_skl_s04",
        "BerkeleyMHAD_skl_s05",
        "BerkeleyMHAD_skl_s06",
        "BerkeleyMHAD_skl_s07",
        "BerkeleyMHAD_skl_s08",
    ],    
    "corps_name_1": [
        "AJ",
        "BigVegas",
        "Kaya",
        "SportyGranny",
    ]
}
test_set = {
    "corps_BerkeleyMHAD": [
        "BerkeleyMHAD_skl_s09",
        "BerkeleyMHAD_skl_s10",
        "BerkeleyMHAD_skl_s11",
        "BerkeleyMHAD_skl_s12",
    ],
}
def get_character_names(args):
    characters = {}
    if args.is_train:
        """
        Put the name of subdirectory in retargeting/datasets/Mixamo as [[names of group A], [names of group B]]
        """
        characters = get_train_list()
    else:
        """
        To run evaluation successfully, number of characters in both groups must be the same. Repeat is okay.
        """
        characters = {
        "corps_BerkeleyMHAD": [
            "BerkeleyMHAD_skl_s05",
            "BerkeleyMHAD_skl_s06",
        ],
        "corps_motion_project": [
            "Female1",
            "Female1"
        ],
    }
    
    import itertools as it
    topo = []
    for key in characters.values():
        topo.append(key)
    topo = [list(x) for x in it.permutations(topo, 2)]
    return topo


def create_dataset(args, character_names=None):
    from datasets.combined_motion import TestData, MixedData
    if args.is_train:
        return MixedData(args, character_names, get_train_list())
    else:
        return TestData(args, character_names, get_train_list())


def get_test_set():
    return test_set


def get_train_list():
    return train_set
    
