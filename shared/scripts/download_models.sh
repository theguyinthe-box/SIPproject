#! /bin/bash

#Locations for the models to be downloaded to
# model/pretrained_models 
#    - shape predictor
#    - ffhq 1024
#    - We only need one of these but we will sort that out later
#    - restyle_psp_ffhq 
#    - restyle_e4e_ffhq 

#We also need to download the boundarys that we are gonna be using
# The repo already expects them to be in model/editing/interfacegan/boundaries so we will download them there
# We wanna gdown from this gdrive folder https://drive.google.com/drive/folders/1tzlY5MY2P6dr9dCnBc7a-9RUs6zUxh3E
# These are reference in the stylegan3-editing readme file
