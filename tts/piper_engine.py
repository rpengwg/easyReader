import threading
import wave
from pathlib import Path

from core.logger import logger
from core.paths import TEMP_DIR
from tts.model_loader import ModelLoader


class PiperEngine:
    def __init__(self):
        self.lock = threading.Lock()
        self.voice = None
        self.index = 0
        self.loader = ModelLoader()

    def _load_voice(self):
        if self.voice:
            return self.voice
        try:
            from piper import PiperVoice
            model = self.loader.get_model()
            self.voice = PiperVoice.load(str(model))
            logger.info("Piper model loaded: %s", model)
            return self.voice
        except Exception as exc:
            logger.exception("Piper model load failed: %s", exc)
            raise

    def generate(self, text):
        with self.lock:
            try:
                voice = self._load_voice()
                self.index += 1
                output = TEMP_DIR / f"speech_{self.index}.wav"
                with wave.open(str(output), "wb") as wav:
                    voice.synthesize_wav(text, wav)
                return str(output)
            except Exception as exc:
                logger.error("speech generation failed: %s", exc)
                return None
