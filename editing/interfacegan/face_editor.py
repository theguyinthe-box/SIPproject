from typing import Optional, Tuple

import numpy as np
import torch
import random

from configs.paths_config import interfacegan_aligned_edit_paths, interfacegan_unaligned_edit_paths
from models.stylegan3.model import GeneratorType
from models.stylegan3.networks_stylegan3 import Generator
from utils.common import tensor2im, generate_random_transform


class FaceEditor:

    def __init__(self, stylegan_generator: Generator, generator_type=GeneratorType.ALIGNED):
        self.generator = stylegan_generator
        if generator_type == GeneratorType.ALIGNED:
            paths = interfacegan_aligned_edit_paths
        else:
            paths = interfacegan_unaligned_edit_paths

        # Load all available direction boundaries and normalize keys to lowercase
        self.interfacegan_directions = {}
        for name, p in paths.items():
            try:
                vec = torch.from_numpy(np.load(p))
            except Exception as e:
                raise RuntimeError(f"Failed loading interfacegan boundary '{p}': {e}")
            # move to GPU if available
            if torch.cuda.is_available():
                vec = vec.cuda()
            self.interfacegan_directions[name.lower()] = vec

    def edit(self, latents: torch.tensor, direction: str, factor: int = 1, factor_range: Optional[Tuple[int, int]] = None,
             user_transforms: Optional[np.ndarray] = None, apply_user_transformations: Optional[bool] = False):
        edit_latents = []
        edit_images = []
        # Normalize lookup to lowercase to match loaded keys
        direction = self.interfacegan_directions[direction.lower()]
        if factor_range is not None:  # Apply a range of editing factors. for example, (-5, 5)
            for f in range(*factor_range):
                edit_latent = latents + f * direction
                edit_image, _, user_transforms = self._latents_to_image(edit_latent,
                                                                     apply_user_transformations,
                                                                     user_transforms)
                edit_latents.append(edit_latent)
                edit_images.append(edit_image)
        else:
            edit_latents = latents + factor * direction
            edit_images, _, _ = self._latents_to_image(edit_latents, apply_user_transformations)
        return edit_images, edit_latents
    
    def edit_random(self, latents: torch.tensor, direction: str, factor: int = 1, factor_range: Optional[Tuple[int, int]] = None,
            image_count: int = 1, user_transforms: Optional[np.ndarray] = None, apply_user_transformations: Optional[bool] = False):
        edit_latents = []
        edit_images = []
        factors_used = []
        edit_tensors = []
        # Normalize lookup to lowercase to match loaded keys
        direction = self.interfacegan_directions[direction.lower()]
        if factor_range is not None:  # Apply a range of editing factors. for example, (-5, 5)
            for f in range(image_count):
                factor = random.uniform(factor_range[0], factor_range[1])
                edit_latent = latents +  factor * direction
                edit_image, edit_tensor, user_transforms = self._latents_to_image(edit_latent,
                                                                     apply_user_transformations,
                                                                     user_transforms)
                factors_used.append(factor)
                edit_latents.append(edit_latent)
                edit_images.append(edit_image)
                edit_tensors.append(edit_tensor)
        else:
            edit_latents = latents + factor * direction
            edit_images, edit_tensors, _ = self._latents_to_image(edit_latents, apply_user_transformations)
            factors_used = factor
        return edit_images, edit_tensors, edit_latents, factors_used

    def _latents_to_image(self, all_latents: torch.tensor, apply_user_transformations: bool = False,
                          user_transforms: Optional[torch.tensor] = None):
        with torch.no_grad():
            if apply_user_transformations:
                if user_transforms is None:
                    # if no transform provided, generate a random transformation
                    user_transforms = generate_random_transform(translate=0.3, rotate=25)
                # apply the user-specified transformation
                if type(user_transforms) == np.ndarray:
                    user_transforms = torch.from_numpy(user_transforms)
                self.generator.synthesis.input.transform = user_transforms.cuda().float()
            # generate the images
            images_tensors = self.generator.synthesis(all_latents, noise_mode='const')
            images = [tensor2im(image) for image in images_tensors]
        return images, images_tensors, user_transforms
