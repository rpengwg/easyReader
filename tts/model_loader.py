from pathlib import Path

from core.paths import MODEL_DIR


class ModelLoader:
    def __init__(self, model_dir=MODEL_DIR, voice=""):
        self.model_dir = Path(model_dir).expanduser()
        self.voice = voice or ""

    def configure(self, model_dir=None, voice=None):
        if model_dir is not None:
            self.model_dir = Path(model_dir).expanduser()
        if voice is not None:
            self.voice = voice

    def list_models(self):
        if not self.model_dir.exists():
            return []
        return sorted(self.model_dir.glob("*.onnx"), key=lambda p: p.name.lower())

    def get_model(self):
        models = self.list_models()
        if not models:
            raise FileNotFoundError(f"No Piper model found: {self.model_dir}")
        if self.voice:
            selected = self.model_dir / self.voice
            if selected.exists() and selected.suffix.lower() == ".onnx":
                return selected
        return models[0]
