import json
from pathlib import Path

from core.paths import ROOT_DIR, MODEL_DIR

SETTINGS_FILE = ROOT_DIR / "config" / "settings.json"

DEFAULTS = {
    "app": {"name": "EasyReader", "version": "1.1.2"},
    "tts": {
        "engine": "piper",
        "model_dir": str(MODEL_DIR),
        "voice": "",
        "speed": 1.0,
        "volume": 1.0,
    },
    "logging": {"level": "INFO", "file": "logs/easyreader.log"},
}


def _merge(default, current):
    if isinstance(default, dict) and isinstance(current, dict):
        result = dict(default)
        for key, value in current.items():
            result[key] = _merge(result[key], value) if key in result else value
        return result
    return current


class Settings:
    def __init__(self, path=SETTINGS_FILE):
        self.path = Path(path)
        self.data = self.load()

    def load(self):
        try:
            if self.path.exists():
                with self.path.open("r", encoding="utf-8") as f:
                    return _merge(DEFAULTS, json.load(f))
        except Exception:
            pass
        return _merge(DEFAULTS, {})

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        tmp.replace(self.path)

    @property
    def tts(self):
        return self.data["tts"]

    def update_tts(self, model_dir, voice, speed, volume):
        self.tts.update({
            "model_dir": str(Path(model_dir).expanduser()),
            "voice": voice,
            "speed": float(speed),
            "volume": float(volume),
        })
        self.save()
