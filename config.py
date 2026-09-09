import sys
import tempfile
from pathlib import Path

APP_NAME = "EasyReader"
APP_VERSION = "1.0.0"
MODEL_NAME = "zh_CN-huayan-medium"

# Source mode and PyInstaller one-folder mode use different resource roots.
if getattr(sys, "frozen", False):
    RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
else:
    RESOURCE_DIR = Path(__file__).resolve().parent

MODEL_DIR = RESOURCE_DIR / "models"
TEMP_DIR = Path(tempfile.gettempdir()) / "EasyReader"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

PIPER_MODEL = MODEL_DIR / f"{MODEL_NAME}.onnx"
PIPER_CONFIG = MODEL_DIR / f"{MODEL_NAME}.onnx.json"

SELECTION_DELAY = 0.25
COPY_WAIT = 0.12
MIN_TEXT_LENGTH = 2
MAX_CHUNK_LENGTH = 350
MAX_TEXT_LENGTH = 200000
