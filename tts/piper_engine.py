import threading
import wave
from pathlib import Path

from core.logger import logger
from core.paths import TEMP_DIR, MODEL_DIR
from tts.model_loader import ModelLoader


class PiperEngine:
    def __init__(self, model_dir=MODEL_DIR, voice="", speed=1.0, volume=1.0):
        self.lock = threading.Lock()
        self.voice = None
        self.index = 0
        self.speed = float(speed)
        self.volume = float(volume)
        self.loader = ModelLoader(model_dir, voice)

    def configure(self, model_dir=None, voice=None, speed=None, volume=None):
        with self.lock:
            old_model = self.loader.get_model() if self.loader.list_models() else None
            self.loader.configure(model_dir, voice)
            if speed is not None:
                self.speed = max(0.5, min(2.0, float(speed)))
            if volume is not None:
                self.volume = max(0.0, min(2.0, float(volume)))
            new_model = self.loader.get_model() if self.loader.list_models() else None
            if old_model != new_model:
                self.voice = None
                logger.info("Piper voice changed: %s", new_model)

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
                    try:
                        from piper import SynthesisConfig
                        config = SynthesisConfig(
                            volume=self.volume,
                            length_scale=1.0 / self.speed,
                        )
                        voice.synthesize_wav(text, wav, syn_config=config)
                    except (ImportError, TypeError):
                        # Keep compatibility with older Piper releases.
                        voice.synthesize_wav(text, wav)
                return str(output)
            except Exception as exc:
                logger.error("speech generation failed: %s", exc)
                return None
