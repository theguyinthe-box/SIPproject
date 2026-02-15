import os # For Debugging
import pdb
import sys
import time
from typing import Optional

import numpy as np
import pyrallis
import torch
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from tqdm import tqdm
from tqdm.contrib import tenumerate
sys.path.append(".")
sys.path.append("..")

from configs import data_configs
from inversion.datasets.inference_dataset import InferenceDataset
from editing.interfacegan.face_editor import FaceEditor
from inversion.options.test_options import TestOptions
from models.stylegan3.model import GeneratorType
from utils.common import tensor2im
from utils.inference_utils import get_average_image, run_on_batch, load_encoder
from model.criteria.lpips.lpips import LPIPS
from model.criteria.ms_ssim import MSSSIM

@pyrallis.wrap()
def run(test_opts: TestOptions):

    out_path_results = test_opts.output_path
    out_path_results.mkdir(exist_ok=True, parents=True)

    # update test options with options used during training
    net, opts = load_encoder(checkpoint_path=test_opts.checkpoint_path, test_opts=test_opts)

    print(f'Loading dataset for {opts.dataset_type}')
    dataset_args = data_configs.DATASETS[opts.dataset_type]
    transforms_dict = dataset_args['transforms'](opts).get_transforms()
    dataset = InferenceDataset(root=opts.data_path,
                               landmarks_transforms_path=opts.landmarks_transforms_path,
                               transform=transforms_dict['transform_inference'])
    dataloader = DataLoader(dataset,
                            batch_size=opts.test_batch_size,
                            shuffle=False,
                            num_workers=int(opts.test_workers),
                            drop_last=False)
    
    gt_ims = [Image.open(path).convert('RGB') for path in opts.data_path.glob('*')]
    gt_tensors = [transforms_dict["transform_source"](gt_im).cuda() for gt_im in gt_ims]

    if opts.n_images is None:
        opts.n_images = len(dataset)

    # prepare editing directions and ranges
    latent_editor = FaceEditor(net.decoder, generator_type=GeneratorType.ALIGNED)

    avg_image = get_average_image(net)

    #resize_amount = (256, 256) if opts.resize_outputs else (opts.output_size, opts.output_size)

    lpips = LPIPS(net_type='alex').cuda()
    l2 = torch.nn.MSELoss().cuda()
    msssim = MSSSIM().cuda()

    global_i = 0
    global_time = []
    for input_batch in dataloader:
        if global_i >= opts.n_images:
            break
        with torch.no_grad():
            input_batch, landmarks_transform = input_batch
            tic = time.time()
            result_batch, results_tensors_batch, factors_batch = edit_batch(inputs=input_batch.cuda().float(),
                                      net=net,
                                      avg_image=avg_image,
                                      latent_editor=latent_editor,
                                      opts=opts,
                                      landmarks_transform=landmarks_transform.cuda().float())
            toc = time.time()
            global_time.append(toc - tic)

        for i in range(input_batch.shape[0]):
            
            im_path = dataset.paths[global_i]
            results = result_batch[i]
            tensors = results_tensors_batch[i]
            factors = factors_batch[i]

            inversion = results.pop('inversion') # We still need this cause it removes it from the results dict
            #input_im = tensor2im(input_batch[i])

            for edit_name, edit_res in results.items():
                print(f"Saving edits for {im_path.name} in direction {edit_name}")
                for idx, result in tenumerate(edit_res, ascii=True): # Save each edited image separately
                    computed_lpips = compute_loss(tensors[edit_name][idx], gt_tensors[global_i], lpips)
                    computed_l2 = compute_loss(tensors[edit_name][idx], gt_tensors[global_i], l2)
                    computed_msssim = compute_loss(tensors[edit_name][idx].unsqueeze(0), gt_tensors[global_i].unsqueeze(0), msssim)
                    metadata = PngInfo()
                    metadata.add_text("edit_direction", edit_name)
                    metadata.add_text("edit_factor", str(factors[edit_name][idx]))
                    metadata.add_text("computed_lpips", str(computed_lpips))
                    metadata.add_text("computed_l2", str(computed_l2))
                    metadata.add_text("computed_msssim", str(computed_msssim))
                    edit_save_dir = out_path_results
                    edit_save_dir.mkdir(exist_ok=True, parents=True)
                    result.save(edit_save_dir / f"{edit_name}_{im_path.stem}_{idx}.png", pnginfo=metadata, compress_level=0)
            global_i += 1

    #stats_path = opts.output_path / 'stats.txt'
    result_str = f'Runtime {np.mean(global_time):.4f}+-{np.std(global_time):.4f}'
    print(result_str)

    #with open(stats_path, 'w') as f:
    #    f.write(result_str)


def edit_batch(inputs: torch.tensor, net, avg_image: torch.tensor, latent_editor: FaceEditor, opts: TestOptions,
               landmarks_transform: Optional[torch.tensor] = None):
    
    y_hat, latents = get_inversions_on_batch(inputs=inputs,
                                             net=net,
                                             avg_image=avg_image,
                                             opts=opts,
                                             landmarks_transform=landmarks_transform)
    
    # store all results for each sample, split by the edit direction
    results = {idx: {'inversion': tensor2im(y_hat[idx])} for idx in range(len(inputs))}
    results_factors = {idx: {} for idx in range(len(inputs))}  # to store the factors used for each edit
    results_tensors = results_tensors = {idx: {'inversion': y_hat[idx]} for idx in range(len(inputs))} # to store the edited tensors for loss computation
    
    #This runs once in each direction
    for edit_direction, factor_range in zip(opts.edit_directions, opts.factor_ranges):
        #print(f"Applying edits in direction {edit_direction} with factor range {factor_range}")
        edit_res = latent_editor.edit_random(latents=latents,
                                      direction=edit_direction,
                                      factor_range=factor_range,
                                      image_count=opts.n_edited_images_per_direction,
                                      apply_user_transformations=True,
                                      user_transforms=landmarks_transform)
        edit_images, edit_tensors, edit_latents, factors_used = edit_res
        # store the results for each sample
        for idx in range(inputs.shape[0]):
            results[idx][edit_direction] = [step_res[idx] for step_res in edit_images]
            results_tensors[idx][edit_direction] = [step_res[idx] for step_res in edit_tensors] # store the edited tensors for this sample
            results_factors[idx][edit_direction] = factors_used
    return results, results_tensors, results_factors

# gt_image is the ground truth image tensor
def compute_loss(inference, gt, loss_func) -> float:
    loss = float(loss_func(inference, gt))
    return loss

def get_inversions_on_batch(inputs: torch.tensor, net, avg_image: torch.tensor, opts: TestOptions,
                            landmarks_transform: Optional[torch.tensor] = None):
    result_batch, result_latents = run_on_batch(inputs=inputs,
                                                net=net,
                                                opts=opts,
                                                avg_image=avg_image,
                                                landmarks_transform=landmarks_transform)
    # we'll take the final inversion as the inversion to edit
    y_hat = [result_batch[idx][-1] for idx in range(len(result_batch))]
    latents = [torch.from_numpy(result_latents[idx][-1]).cuda() for idx in range(len(result_batch))]
    return y_hat, torch.stack(latents)

if __name__ == '__main__':
    run()
