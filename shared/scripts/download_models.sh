#! /bin/bash

#Locations for the models to be downloaded to
# model/pretrained_models 
#    - shape predictor
#    - ffhq 1024
#    - We only need one of these but we will sort that out later
#    - restyle_psp_ffhq 
#    - restyle_e4e_ffhq 

# sg3-r-ffhq-1024.pt
wget "https://drive.usercontent.google.com/download?id=12WZi2a9ORVg-j6d9x4eF-CKpLaURC2W-&export=download&authuser=0&confirm=t&uuid=bc6e4d9e-eee3-4ac3-ad3e-e658258d196e&at=APcXIO0V-wsFwQdjvll9sHk8Mq5e%3A1770869336745" \ 
-O restyle_pSp_ffhq.pt 

# restyle_e4e_ffhq.pt
wget "https://drive.usercontent.google.com/download?id=1z_cB187QOc6aqVBdLvYvBjoc93-_EuRm&export=download&authuser=0&confirm=t&uuid=821e20b0-3720-4f1a-9ab5-fb168ab30519&at=APcXIO1_fBIrWAgmtvEJ5gITQRRm%3A1770869256223" \
-O restyle_e4e_ffhq.pt

# sg3-r-ffhq-1024.pt
wget "https://drive.usercontent.google.com/download?id=13q6m-bpe3Ws9en9y45JEx2PHQirStt8N&export=download&authuser=0&confirm=t&uuid=41a5631b-c3ad-4111-a952-efb77717b77a&at=APcXIO3bruEk7mCgr7nWCkatkmhg%3A1770869743209" \
-O sg3-r-ffhq-1024.pt

#We also need to download the boundarys that we are gonna be using
# The repo already expects them to be in model/editing/interfacegan/boundaries so we will download them there
# We wanna gdown from this gdrive folder https://drive.google.com/drive/folders/1tzlY5MY2P6dr9dCnBc7a-9RUs6zUxh3E
# These are reference in the stylegan3-editing readme file
gdown --folder https://drive.google.com/drive/folders/1tzlY5MY2P6dr9dCnBc7a-9RUs6zUxh3E -O model/editing/interfacegan/boundaries/ffhq