import numpy as np
import os
from checkpointer import Checkpointer
from defaults import get_cfg_defaults
from model import Model
from imageHandler import align_image
from alter_images import alter



RAW_IMG_DIR = '../shared/Camera'
ALIGNED_IMG_DIR = '../shared/aligned'
ALTERED_IMG_DIR = '../shared/altered'
IMG_VECTOR_DIR = '../shared/alignmentVector'

def __main__():
    
    #align raw image and get vector 
    align_image(RAW_IMG_DIR,ALIGNED_IMG_DIR,IMG_VECTOR_DIR)

    #instantiate model
    cfg = get_cfg_defaults()

    model = Model(
        startf=cfg.MODEL.START_CHANNEL_COUNT,
        layer_count=cfg.MODEL.LAYER_COUNT,
        maxf=cfg.MODEL.MAX_CHANNEL_COUNT,
        latent_size=cfg.MODEL.LATENT_SPACE_SIZE,
        truncation_psi=cfg.MODEL.TRUNCATIOM_PSI,
        truncation_cutoff=cfg.MODEL.TRUNCATIOM_CUTOFF,
        mapping_layers=cfg.MODEL.MAPPING_LAYERS,
        channels=cfg.MODEL.CHANNELS,
        generator=cfg.MODEL.GENERATOR,
        encoder=cfg.MODEL.ENCODER)
    
    model.requires_grad_(False)

    decoder = model.decoder()
    encoder = model.encoder()
    mapping_tl = model.mapping_d()
    mapping_fl = model.mapping_f()
    dlatent_avg = model.dlatent_avg()

    arguments = dict()
    arguments["iteration"] = 0

    model_dict = {
        'discriminator_s': encoder,
        'generator_s': decoder,
        'mapping_tl_s': mapping_tl,
        'mapping_fl_s': mapping_fl,
        'dlatent_avg': dlatent_avg
    }

    checkpointer = Checkpointer(cfg,
                            model_dict,
                            {},
                            save=False)

    #set 
    model.eval()

    path = ALIGNED_IMG_DIR

    paths = list(os.listdir(path))
    paths.sort()
    paths_backup = paths[:]    

    W = [torch.tensor(np.load("principal_directions/direction_%d.npy" % i), dtype=torch.float32) for i in indices]