import os
from pathlib import Path

from core.paths import (
    BASE_DIR,
    MODEL_DIR,
    TEMP_DIR,
    LOG_DIR,
)


APP_NAME = "EasyReader"
APP_VERSION = "1.1.2"


# v1.1.2 compatibility layer
# Keep old modules working while moving runtime settings into core/paths.py

MODEL_NAME = os.getenv(
    "EASYREADER_MODEL",
    "zh_CN-huayan-medium.onnx"
)

PIPER_MODEL = MODEL_DIR / MODEL_NAME
PIPER_CONFIG = Path(str(PIPER_MODEL) + ".json")


MIN_TEXT_LENGTH = 1
MAX_TEXT_LENGTH = 5000
SELECTION_DELAY = 0.3


# Runtime options
PIPER_SPEED = float(os.getenv("EASYREADER_SPEED", "1.0"))
PIPER_VOLUME = float(os.getenv("EASYREADER_VOLUME", "1.0"))


SETTINGS_FILE = BASE_DIR / "config" / "settings.json"

__all__ = [
    "APP_NAME",
    "APP_VERSION",
    "PIPER_MODEL",
    "PIPER_CONFIG",
    "MODEL_DIR",
    "TEMP_DIR",
    "LOG_DIR",
    "SETTINGS_FILE",
    "MIN_TEXT_LENGTH",
    "MAX_TEXT_LENGTH",
    "SELECTION_DELAY",
]
