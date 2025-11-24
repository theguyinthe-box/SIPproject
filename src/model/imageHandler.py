import glob,os
import PIL.Image

RAW_IMG_PATH = "../shared"
ALIGNED_IMG_PATH = "../shared/aligned"
VALID_IMG_EXT = (".jpg",".png")

def load_raw():
    for f in os.listdir(RAW_IMG_PATH):
        if f.endswith(VALID_IMG_EXT):
            img = PIL.Image.open(RAW_IMG_PATH + f)
    return img

def load_aligned():
    for f in os.listdir(ALIGNED_IMG_PATH):
        if f.endswith(VALID_IMG_EXT):
            img = PIL.Image.open(ALIGNED_IMG_PATH + f)
    return img
