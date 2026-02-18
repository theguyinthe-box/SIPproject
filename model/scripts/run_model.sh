#! /bin/bash
cd /workspace
TIMEFORMAT=%lE

START_TIME=$SECONDS
#Now we to prepare our data, what we need to do here can be found in model/readme
# the source image folder needs to be "Camera" because that is what ADB will save the images to, for some odd reason I can't change that so we live with it
python prepare_data/preparing_faces_parallel.py --mode align --root_path data/Camera

# we for some reason need to do both?
python prepare_data/preparing_faces_parallel.py --mode crop --root_path data/Camera --random_shift 0.05

#Compute the landmarks transforms for the images we are going to be using, this is needed for the editing script
time python prepare_data/compute_landmarks_transforms.py \
--raw_root data/Camera \
--aligned_root data/Camera_aligned \
--cropped_root data/Camera_croped \
--output_root data/landmarks_transforms/

#Run the the model with their edit image script
time LANG=en_US.utf8 python inversion/scripts/inference_editing_random.py \
--output_path data/test \
--checkpoint_path pretrained_models/restyle_pSp_ffhq.pt \
--data_path data/Camera_aligned \
--test_batch_size 4 \
--test_workers 4 \
--n_iters_per_batch 3 \
--edit_directions "[age,pose,smiling]" \
--factor_ranges "[(-5_5),(-5_5),(-5_5)]" \
--landmarks_transforms_path data/landmarks_transforms/landmarks_transforms.npy \
--n_edited_images_per_direction 10

echo "Time taken: $(( SECONDS - START_TIME )) seconds"
