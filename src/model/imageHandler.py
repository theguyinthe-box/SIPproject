import glob,os
import PIL.Image
from ffhq_dataset.face_alignment import image_align
from ffhq_dataset.landmarks_detector import LandmarksDetector

RAW_IMG_PATH = "../shared/Camera"
ALIGNED_IMG_PATH = "../shared/aligned"
VECTOR_PATH = '../shared/alignment_vector'
VALID_IMG_EXT = (".jpg",".png")

def align_image():
    landmarks_model_path = './shape_predictor_81_face_landmarks.dat'
    landmarks_detector = LandmarksDetector(landmarks_model_path)
    for img_name in [x for x in os.listdir(RAW_IMG_PATH) if x[0] not in '._']:
        raw_img_path = os.path.join(RAW_IMG_PATH, img_name)
        for i, face_landmarks in enumerate(landmarks_detector.get_landmarks(raw_img_path), start=1):
            face_img_name = '%s_%02d' % (os.path.splitext(img_name)[0], i)
            aligned_face_path = os.path.join(ALIGNED_IMG_PATH, face_img_name)
            vector_path = os.path.join(VECTOR_PATH, face_img_name)
            os.makedirs(ALIGNED_IMG_PATH, exist_ok=True)
            image_align(raw_img_path, aligned_face_path, vector_path, face_landmarks)