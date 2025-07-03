from pathlib import Path


# PROJECT ROOT: ga uit van de repo root, automatisch gedetecteerd
PROJECT_ROOT = Path(__file__).resolve().parent


# Data directories
DATASETS = PROJECT_ROOT / "Datasets"
TRAIN = DATASETS / "Train_data"
TEST = DATASETS / "Test_data"
EVAL = DATASETS / "Eval_data"

COMBO_DATA = DATASETS / "combo_overlay_sets"
COMBO_TRAIN = COMBO_DATA / "Train"
COMBO_TEST = COMBO_DATA / "Test"

MASKRCNN_RESEARCH_DATASET = PROJECT_ROOT / "ModelResearch" / "OnderzoekDataSubset"
MASKRCNN_RESEARCH_TRAIN = MASKRCNN_RESEARCH_DATASET / "Train"
MASKRCNN_RESEARCH_TEST = MASKRCNN_RESEARCH_DATASET / "Test"

YOLO_RESEARCH_PATH = PROJECT_ROOT / "ModelResearch" / "Yolo"
YOLO_RESEARCH_DATASET = YOLO_RESEARCH_PATH / "OnderzoekDataSubsetYolo"
YOLO_RESEARCH_TRAIN = YOLO_RESEARCH_DATASET / "Train"
YOLO_RESEARCH_VAL = YOLO_RESEARCH_DATASET / "Val"


# Yaml files
YOLO_DATASET_YAML = PROJECT_ROOT / "ModelResearch" / "Yolo" / "dataset_path.yaml"


# Image examples
YOLO_MASK_EXAMPLE = YOLO_RESEARCH_PATH / "1_image.png"
YOLO_IMAGE_EXAMPLE = YOLO_RESEARCH_PATH / "1_mask.png"
TRANSFORM_IMAGE_EXAMPLE = PROJECT_ROOT / "TransformTest" / "22_image.png"

# Text files
YOLO_ANNOTATION_EXAMPLE = YOLO_RESEARCH_PATH / "generated_yolo_annotation.txt"


# Mask-RCNN models
MODELS_DIR = PROJECT_ROOT / "Models"
MODEL_PATH = MODELS_DIR / "<insert model name here>"


# Yolo subset output creation
YOLO_RESEARCH_DATASET.mkdir(exist_ok=True)


# Model directory output creation
MODELS_DIR.mkdir(exist_ok=True)
