
import torch.utils.data
from model import Model
from launcher import run
from checkpointer import Checkpointer
from dlutils.pytorch import count_parameters
from defaults import get_cfg_defaults
import lreq
import numpy as np

from PIL import Image
from defaults import get_cfg_defaults
from model import Model
from imageHandler import align_image
from alter_images import alter

RAW_IMG_DIR = '../shared/Camera'
ALIGNED_IMG_DIR = '../shared/aligned'
ALTERED_IMG_DIR = '../shared/altered'
IMG_VECTOR_DIR = '../shared/alignmentVector'
TEST_IMG_DIR = '../shared/test'

def __main__():
    #define helper functions
    def encode(x):
        Z, _ = model.encode(x, layer_count-1, 1)
        Z = Z.repeat(1, model.mapping_f.num_layers, 1)
        return Z
    
    def decode(x):
        return model.decoder(x, layer_count-1, 1, noise = True)

    def load(path):
        img = np.asarray(Image.open(path))

        if img.shape[2] == 4:
            img = img[:, :, :3]
        im = img.transpose((2, 0, 1))
        x = torch.tensor(np.asarray(im, dtype=np.float32), requires_grad=True) / 127.5 - 1.
        if x.shape[0] == 4:
            x = x[:3]

        needed_resolution = model.decoder.layer_to_resolution[-1]
        while x.shape[2] > needed_resolution:
            x = F.avg_pool2d(x, 2, 2)
        if x.shape[2] != needed_resolution:
            x = F.adaptive_avg_pool2d(x, (needed_resolution, needed_resolution))

        img_src = ((x * 0.5 + 0.5) * 255).type(torch.long).clamp(0, 255).cpu().type(torch.uint8).transpose(0, 2).transpose(0, 1).numpy()

        latents_original = encode(x[None, ...])
        latents = latents_original[0, 0].clone()
        latents -= model.dlatent_avg.buff.data[0]
        return latents, latents_original, img_src

    def update_image(w, latents_original):
        with torch.no_grad():
            w = w + model.dlatent_avg.buff.data[0]
            w = w[None, None, ...].repeat(1, model.mapping_f.num_layers, 1)
            layer_idx = torch.arange(model.mapping_f.num_layers)[np.newaxis, :, np.newaxis]
            cur_layers = (7 + 1) * 2
            mixing_cutoff = cur_layers
            styles = torch.where(layer_idx < mixing_cutoff, w, latents_original)
            x_rec = decode(styles)
            resultsample = ((x_rec * 0.5 + 0.5) * 255).type(torch.long).clamp(0, 255)
            resultsample = resultsample.cpu()[0, :, :, :]
        return resultsample.type(torch.uint8).transpose(0, 2).transpose(0, 1)


    #instantiate model
    cfg = get_cfg_defaults()

    torch.cuda.set_device(0)

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
        encoder=cfg.MODEL.ENCODER )
    
    model.cuda(0)
    model.eval()
    model.requires_grad_(False)

    decoder = model.decoder
    encoder = model.encoder
    mapping_tl = model.mapping_d
    mapping_fl = model.mapping_f
    dlatent_avg = model.dlatent_avg

    logger.info("Trainable parameters generator:")
    count_parameters(decoder)

    logger.info("Trainable parameters discriminator:")
    count_parameters(encoder)

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
                            logger=logger,
                            save=False)

    extra_checkpoint_data = checkpointer.load()
    #set model to evaluation mode
    model.eval()

    #align raw image and get vector 
    align_image(RAW_IMG_DIR,ALIGNED_IMG_DIR,IMG_VECTOR_DIR)

    layer_count = cfg.MODEL.LAYER_COUNT
    
    path = ALIGNED_IMG_DIR

    latent, latent_original, _ = load(path)   

    altered_img = Image.fromarray(update_image(latent, latent_original))

    altered_img.save(ALTERED_IMG_DIR + "altered_img.jpg")
    
