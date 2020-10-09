def create_model(args, character_names, dataset):
    if args.model == "mul_top_mul_ske":
        args.skeleton_info = "concat"
        import models.architecture
        gan = models.architecture.GAN_model(args, character_names, dataset)
        return gan

    else:
        raise Exception("Unimplemented model")
