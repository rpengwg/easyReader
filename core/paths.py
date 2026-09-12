from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT_DIR / "models" / "piper"
TEMP_DIR = ROOT_DIR / "temp"
LOG_DIR = ROOT_DIR / "logs"
CONFIG_DIR = ROOT_DIR / "config"

for _path in (MODEL_DIR, TEMP_DIR, LOG_DIR, CONFIG_DIR):
    _path.mkdir(parents=True, exist_ok=True)
