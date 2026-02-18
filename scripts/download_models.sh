#! /bin/bash

START_TIME=$SECONDS
#This for some reason beyond me does not work in the dockerfile

#Locations for the models to be downloaded to
# model/pretrained_models 

#restyle_pSp_ffhq.pt
gdown -c 12WZi2a9ORVg-j6d9x4eF-CKpLaURC2W- -O ../model/pretrained_models/restyle_pSp_ffhq.pt

# restyle_e4e_ffhq.pt
gdown -c 1z_cB187QOc6aqVBdLvYvBjoc93-_EuRm -O ../model/pretrained_models/restyle_e4e_ffhq.pt

# sg3-r-ffhq-1024.pt
gdown -c 13q6m-bpe3Ws9en9y45JEx2PHQirStt8N -O ../model/pretrained_models/sg3-r-ffhq-1024.pt

# sg3-r-ffhqu-1024.pt
gdown -c 1Xfi0mBgiDb8AUazWok9eKSRQon9YVMMW -O ../model/pretrained_models/sg3-r-ffhqu-1024.pt

#We also need to download the boundarys that we are gonna be using
# The repo already expects them to be in model/editing/interfacegan/boundaries so we will download them there
# We wanna gdown from this gdrive folder https://drive.google.com/drive/folders/1tzlY5MY2P6dr9dCnBc7a-9RUs6zUxh3E
# These are reference in the stylegan3-editing readme file
gdown --folder -c https://drive.google.com/drive/folders/1tzlY5MY2P6dr9dCnBc7a-9RUs6zUxh3E -O ../model/editing/interfacegan/boundaries/ffhq
gdown --folder -c https://drive.google.com/drive/folders/1AwVxrJe5Pm5GWdqiG-sSfUDzDjidO4cE -O ../model/editing/interfacegan/boundaries/ffhqu

echo "Time taken: $(( SECONDS - START_TIME )) seconds"
