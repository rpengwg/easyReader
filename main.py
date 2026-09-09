import os
import shutil
import sys
import threading
import time

from capture.selection import SelectionMonitor
from config import APP_NAME, APP_VERSION, PIPER_CONFIG, PIPER_MODEL
from control.hotkey import HotkeyController
from tts.piper_engine import PiperEngine
from tts.player import AudioPlayer
from tts.splitter import split_text
from ui.tray import TrayApp


class EasyReader:
    def __init__(self):
        self.tts = PiperEngine()
        self.player = AudioPlayer()
        self.stop_event = threading.Event()
        self.exit_event = threading.Event()
        self.worker = None
        self.selection_monitor = SelectionMonitor(self.on_text_selected)
        self.hotkey = HotkeyController(
            self.player,
            stop_callback=self.stop_reading,
            exit_callback=self.shutdown,
        )
        self.tray = TrayApp(self)

    def validate_model(self):
        return PIPER_MODEL.exists() and PIPER_CONFIG.exists()

    def on_text_selected(self, text):
        self.stop_reading()
        self.worker = threading.Thread(target=self.speak, args=(text,), daemon=True)
        self.worker.start()

    def stop_reading(self):
        self.stop_event.set()
        self.player.stop()

    def toggle_pause(self):
        self.player.pause_resume()

    def speak(self, text):
        self.stop_event.clear()
        chunks = split_text(text)
        for index, chunk in enumerate(chunks, 1):
            if self.stop_event.is_set() or self.exit_event.is_set():
                break
            print(f"朗读第 {index}/{len(chunks)} 段")
            audio_file = self.tts.generate(chunk)
            if not audio_file or self.stop_event.is_set():
                continue
            self.player.play(audio_file)
            while self.player.is_playing() or self.player.paused:
                if self.stop_event.is_set() or self.exit_event.is_set():
                    self.player.stop()
                    break
                time.sleep(0.08)
            try:
                os.remove(audio_file)
            except OSError:
                pass

    def start(self):
        if not self.validate_model():
            print("缺少 Piper 中文模型文件。请使用完整 Release 包。")
            print(PIPER_MODEL)
            return 1
        print(f"{APP_NAME} V{APP_VERSION} 已启动")
        self.selection_monitor.start()
        self.hotkey.start()
        self.tray.run()
        return 0

    def shutdown(self):
        if self.exit_event.is_set():
            return
        self.exit_event.set()
        self.stop_reading()
        self.selection_monitor.stop()
        self.hotkey.stop()
        self.player.stop()
        self.tray.stop()


def main():
    app = EasyReader()
    return app.start()


if __name__ == "__main__":
    raise SystemExit(main())
