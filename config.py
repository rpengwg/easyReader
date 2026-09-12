import os
import sys
from pathlib import Path


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent
    return base / relative


BASE_DIR = resource_path("")

# v1.1.2: models are external runtime assets
# EXE can be replaced without packaging Piper models again.
MODEL_DIR = Path(os.getenv("EASYREADER_MODEL_DIR", BASE_DIR / "models"))

PIPER_MODEL = MODEL_DIR / os.getenv(
    "EASYREADER_MODEL",
    "zh_CN-huayan-medium.onnx"
)

PIPER_CONFIG = Path(str(PIPER_MODEL) + ".json")

TEMP_DIR = Path(os.getenv("EASYREADER_TEMP_DIR", BASE_DIR / "temp"))
TEMP_DIR.mkdir(parents=True, exist_ok=True)

MIN_TEXT_LENGTH = 1
MAX_TEXT_LENGTH = 5000
SELECTION_DELAY = 0.3

APP_NAME = "EasyReader"
APP_VERSION = "1.1.2"
