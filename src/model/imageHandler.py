import os
import paths
from glob import glob
from ffhq_dataset.face_alignment import image_align
from ffhq_dataset.landmarks_detector import LandmarksDetector
from PIL import Image,  ImageOps

def align_image():
    landmarks_detector = LandmarksDetector(paths.LANDMARKS_MODEL_PATH)
    for img_path in [x for x in glob(paths.RAW_IMG_DIR + "/[!.]*")]:
        
        image = Image.open(str(img_path))
        image = ImageOps.exif_transpose(image)
        image.save(img_path)

        for i, face_landmarks in enumerate(landmarks_detector.get_landmarks(img_path), start=1):
            aligned_face_path = os.path.join(paths.ALIGNED_IMG_DIR, "aligned_" + os.path.basename(img_path))
            vector_path = os.path.join(paths.VECTOR_DIR, os.path.basename(img_path))
            os.makedirs(paths.ALIGNED_IMG_DIR, exist_ok=True)
            image_align(img_path, aligned_face_path, vector_path, face_landmarks)