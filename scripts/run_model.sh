#! /bin/bash

#DOWNLOAD THE MODELS AND BOUNDARIES IF THEY ARE NOT PRESENT
bash shared/scripts/download_models.sh

#Install GUI dependencies
#npm install --prefix ./SIP-GUI/ # << This command can be run here or in the dockerfile, SIP-GUI is passed as a volume to the container so it can be run on the host machine as well, we will sort this out later

#Now we to prepare our data, what we need to do here can be found in model/readme
# the source image folder needs to be "Camera" because that is what ADB will save the images to, for some odd reason I can't change that so we live with it
python model/prepare_data/preparing_faces_parallel.py --mode align --root_path /shared/Camera

# we for some reason need to do both?
python model/prepare_data/preparing_faces_parallel.py --mode crop --root_path /shared/Camera --random_shift 0.05

#Compute the landmarks transforms for the images we are going to be using, this is needed for the editing script
python model/prepare_data/compute_landmarks_transforms.py \
--raw_root /shared/Camera \
--aligned_root /shared/Camera_aligned \
--cropped_root /shared/Camera_croped \
--output_root /shared/landmarks_transforms/

#Run the the model with their edit image script
python model/inversion/scripts/inference_editing.py \
--output_path shared/test \
--checkpoint_path model/pretrained_models/restyle_e4e_ffhq.pt \
--data_path /shared/Camera \
--test_batch_size 4 \
--test_workers 4 \
--n_iters_per_batch 3 \
--edit_directions "[age,pose,smile]" \
--factor_ranges "[(-5_5),(-5_5),(-5_5)]" \
--landmarks_transforms_path /shared/landmarks_transforms/landmarks_transforms.npy

