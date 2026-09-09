import os
import sys
from pathlib import Path

APP_NAME = "EasyReader"
APP_VERSION = "1.0.0"

# PyInstaller one-folder release keeps models next to the executable.
def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent

BASE_DIR = get_base_dir()
MODEL_DIR = BASE_DIR / "models"
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "zh_CN-huayan-medium"
PIPER_MODEL = MODEL_DIR / f"{MODEL_NAME}.onnx"
PIPER_CONFIG = MODEL_DIR / f"{MODEL_NAME}.onnx.json"

SELECTION_DELAY = 0.25
COPY_WAIT = 0.12
MIN_TEXT_LENGTH = 2
MAX_CHUNK_LENGTH = 350

# Ignore obvious non-text selections and accidental empty copies.
MAX_TEXT_LENGTH = 200000
