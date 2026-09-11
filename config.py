import os
import sys


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base, relative)


BASE_DIR = resource_path("")

MODEL_DIR = resource_path("models")

PIPER_MODEL = os.path.join(
    MODEL_DIR,
    "zh_CN-huayan-medium.onnx"
)

PIPER_CONFIG = os.path.join(
    MODEL_DIR,
    "zh_CN-huayan-medium.onnx.json"
)

# Text selection limits
# Used by capture.selection to avoid sending empty or extremely large content to TTS
MIN_TEXT_LENGTH = 1
MAX_TEXT_LENGTH = 5000

# Delay after mouse selection before reading clipboard/UIA content
SELECTION_DELAY = 0.3
