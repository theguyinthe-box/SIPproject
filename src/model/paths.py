from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent
RAW_IMG_DIR = str(SRC_DIR / "shared/Camera")
ALIGNED_IMG_DIR = str(SRC_DIR / "shared/aligned")
VECTOR_DIR = str(SRC_DIR / 'shared/alignment_vector')
ALTERED_IMG_DIR = str(SRC_DIR / 'shared/altered')
TEST_IMG_DIR = str(SRC_DIR / 'shared/test')
MODEL_DIR = str(SRC_DIR / "model/training_artifacts/ffhq/model_194.pth")
LANDMARKS_MODEL_PATH = str(SRC_DIR / 'model/shape_predictor_81_face_landmarks.dat')
PRINCIPAL_DIRECTIONS = str(SRC_DIR / 'model/principal_directions')
VALID_IMG_EXT = (".jpg",".png")