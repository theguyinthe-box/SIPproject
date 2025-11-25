import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import torch
from model import Model
from launcher import run
from checkpointer import Checkpointer
import lreq
import logging
import bz2

indices = [0, 1, 2, 3, 4, 10, 11, 17, 19]
W = [torch.tensor(np.load("principal_directions/direction_%d.npy" % i), dtype=torch.float32) for i in indices]

def alter(alteration_vector, input_latent, W):

    altered = input_latent.detach().clone()
    
    altered += alteration_vector * W
    
    im = convert_to_image(altered)
    
    img = Image.fromarray(im.detach().numpy())
    
    generated_image_landmarks = face_recognition.face_landmarks(np.array(img))[0]
        
    lm = np.load(face_landmarks)
    lm_chin = lm[0:17]  # left-right
    lm_eyebrow_left = lm[17:22]  # left-right
    lm_eyebrow_right = lm[22:27]  # left-right
    lm_nose = lm[27:31]  # top-down
    lm_nostrils = lm[31:36]  # top-down
    lm_eye_left = lm[36:42]  # left-clockwise
    lm_eye_right = lm[42:48]  # left-clockwise
    lm_mouth_outer = lm[48:60]  # left-clockwise
    lm_mouth_inner = lm[60:68]  # left-clockwise

    # Calculate auxiliary vectors.
    eye_left = np.mean(lm_eye_left, axis=0)
    eye_right = np.mean(lm_eye_right, axis=0)
    eye_avg = (eye_left + eye_right) * 0.5
    eye_to_eye = eye_right - eye_left
    mouth_left = lm_mouth_outer[0]
    mouth_right = lm_mouth_outer[6]
    mouth_avg = (mouth_left + mouth_right) * 0.5
    eye_to_mouth = mouth_avg - eye_avg

    left_eye_before = np.mean(generated_image_landmarks["left_eye"], axis=0)
    right_eye_before = np.mean(generated_image_landmarks["right_eye"], axis=0)

    x1b, y1b = left_eye_before
    x2b, y2b = right_eye_before

    y1a, x1a = eye_left
    y2a, x2a = eye_right

    # Generate linear system to compute transformation
    a = np.matrix([[-y1b, x1b, 0, 1], [x1b, y1b, 1, 0], [-y2b, x2b, 0, 1], [x2b, y2b, 1, 0]])

    b = np.array([y1a, x1a, y2a, x2a])

    # Solve linear system
    x = np.linalg.solve(a, b)

    # Calc transformation matrix
    transform_matrix = np.matrix([[x[1], -x[0], x[3]], [x[0], x[1], x[2]], [0, 0, 1]])

    transform_matrix = np.array([[x[1], -x[0], x[3]], [x[0], x[1], x[2]], [0, 0, 1]])

    transform_inv = np.linalg.inv(transform_matrix)

    background = Image.open(src_file).convert("RGB")

    foreground = img
    
    mask = Image.open(mask_file).convert("L").resize(foreground.size).filter(ImageFilter.GaussianBlur(20))
    
    foreground = foreground.transform(background.size, PIL.Image.AFFINE, transform_inv.flatten()[:6], resample=Image.NEAREST)    
    mask = mask.transform(background.size, PIL.Image.AFFINE, transform_inv.flatten()[:6], resample=Image.NEAREST)

    background = Image.composite(foreground, background, mask)
    
    size = 512, 512
    background.thumbnail(size, Image.ANTIALIAS)
    
    return background