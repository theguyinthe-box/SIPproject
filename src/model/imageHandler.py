import glob,os
import PIL.Image

img_path = "../shared"
valid_images = (".jpg",".png")

def load_raw():
    for f in os.listdir(img_path):
        if f.endswith(valid_images):
            img = PIL.Image.open(img_path + f)
    return img


