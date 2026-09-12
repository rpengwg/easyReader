from pathlib import Path

from core.paths import MODEL_DIR


class ModelLoader:
    def __init__(self, model_dir=MODEL_DIR):
        self.model_dir = Path(model_dir)

    def get_model(self):
        models = list(self.model_dir.glob("*.onnx"))
        if not models:
            raise FileNotFoundError(f"No Piper model found: {self.model_dir}")
        return models[0]
