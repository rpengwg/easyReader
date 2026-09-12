import os
import time
import threading
from tkinter import messagebox

from core.logger import logger
from core.paths import MODEL_DIR
from core.settings import Settings
from tts.piper_engine import PiperEngine
from tts.player import AudioPlayer
from tts.splitter import split_text
from capture.selection import SelectionMonitor
from control.hotkey import HotkeyController
from ui.tray import TrayApp
from ui.settings_window import SettingsWindow
from core.reader_queue import ReaderQueue


class EasyReader:
    def __init__(self):
        self.settings = Settings()
        tts = self.settings.tts
        self.tts = PiperEngine(
            tts.get("model_dir", MODEL_DIR),
            tts.get("voice", ""),
            tts.get("speed", 1.0),
            tts.get("volume", 1.0),
        )
        self.player = AudioPlayer()
        self.exit_event = threading.Event()
        self.reading_chars = 0
        self.reader_queue = ReaderQueue(self.speak)
        self.selection_monitor = SelectionMonitor(self.on_text_selected)
        self.hotkey = HotkeyController(self.player, self.stop_reading, self.shutdown)
        self.settings_window = SettingsWindow(self)
        self.tray = TrayApp(self)

    def validate_model(self):
        return bool(self.tts.loader.list_models())

    def on_text_selected(self, text):
        if text:
            self.reader_queue.put(text, replace=self.player.is_playing())

    def stop_reading(self):
        self.reader_queue.clear()
        self.player.stop()

    def toggle_pause(self):
        if hasattr(self.player, "toggle_pause"):
            self.player.toggle_pause()

    def open_settings(self):
        threading.Thread(target=self.settings_window.show, daemon=True).start()

    def speak(self, text):
        try:
            for chunk in split_text(text):
                audio = self.tts.generate(chunk)
                if audio:
                    self.player.play(audio)
                    while self.player.is_playing() or self.player.paused:
                        if self.exit_event.is_set():
                            return
                        time.sleep(0.08)
                    try:
                        os.remove(audio)
                    except OSError:
                        pass
        except Exception as exc:
            logger.exception("reader error: %s", exc)

    def start(self):
        if not self.validate_model():
            messagebox.showerror("EasyReader", f"未找到Piper模型:\n{self.tts.loader.model_dir}")
            return 1
        logger.info("EasyReader 1.1.2 started")
        self.reader_queue.start()
        self.selection_monitor.start()
        self.hotkey.start()
        self.tray.run()
        return 0

    def shutdown(self):
        self.exit_event.set()
        self.reader_queue.stop()
        self.selection_monitor.stop()
        self.hotkey.stop()
        self.player.stop()
        self.tray.stop()


def main():
    return EasyReader().start()


if __name__ == "__main__":
    raise SystemExit(main())
