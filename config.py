import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)


TEMP_DIR = os.path.join(
    BASE_DIR,
    "temp"
)


PIPER_MODEL = os.path.join(
    MODEL_DIR,
    "zh_CN-huayan-medium.onnx"
)


PIPER_CONFIG = os.path.join(
    MODEL_DIR,
    "zh_CN-huayan-medium.onnx.json"
)


PIPER_EXE = "piper"


AUDIO_FILE = os.path.join(
    TEMP_DIR,
    "speech.wav"
)


# 鼠标释放后等待多久再读取文字
SELECTION_DELAY = 0.3


# 最少字符数
MIN_TEXT_LENGTH = 2
