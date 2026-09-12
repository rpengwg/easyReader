from pathlib import Path
import json

from config import MODEL_DIR, PIPER_MODEL, PIPER_CONFIG


class ModelManager:
    """Independent Piper model loader.

    Models stay outside the EXE in normal deployment so users can replace
    Piper voices without rebuilding EasyReader.
    """

    def __init__(self):
        self.model_dir = Path(MODEL_DIR)

    def find_model(self):
        model = Path(PIPER_MODEL)
        config = Path(PIPER_CONFIG)

        if model.exists() and config.exists():
            return model, config

        models = list(self.model_dir.glob("*.onnx"))
        if not models:
            return None, None

        model = models[0]
        config = Path(str(model) + ".json")
        return (model, config) if config.exists() else (model, None)

    def validate(self):
        model, config = self.find_model()
        return model is not None and config is not None

    def info(self):
        model, config = self.find_model()
        return {
            "model": str(model) if model else None,
            "config": str(config) if config else None,
        }
