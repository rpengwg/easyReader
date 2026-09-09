import threading
import wave

from config import PIPER_MODEL, TEMP_DIR


class PiperEngine:
    def __init__(self):
        self.lock = threading.Lock()
        self._voice = None
        self._index = 0

    def _load_voice(self):
        if self._voice is not None:
            return self._voice
        if not PIPER_MODEL.exists():
            raise FileNotFoundError(f"未找到 Piper 模型：{PIPER_MODEL}")
        try:
            from piper import PiperVoice
        except ImportError as exc:
            raise RuntimeError("piper-tts 未正确安装或未被打包") from exc
        self._voice = PiperVoice.load(str(PIPER_MODEL))
        return self._voice

    def generate(self, text):
        with self.lock:
            try:
                voice = self._load_voice()
                self._index += 1
                output = TEMP_DIR / f"speech_{self._index}.wav"
                with wave.open(str(output), "wb") as wav_file:
                    voice.synthesize_wav(text, wav_file)
                return str(output)
            except Exception as exc:
                print(f"Piper 语音生成失败：{exc}")
                return None
