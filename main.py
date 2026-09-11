import os
import time
import threading

from capture.selection import SelectionMonitor
from config import APP_NAME, APP_VERSION, PIPER_CONFIG, PIPER_MODEL
from control.hotkey import HotkeyController
from tts.piper_engine import PiperEngine
from tts.player import AudioPlayer
from tts.splitter import split_text
from ui.tray import TrayApp
from core.reader_queue import ReaderQueue


class EasyReader:
    def __init__(self):
        self.tts = PiperEngine()
        self.player = AudioPlayer()
        self.exit_event = threading.Event()

        self.reader_queue = ReaderQueue(self.speak)

        self.selection_monitor = SelectionMonitor(
            self.on_text_selected
        )

        self.hotkey = HotkeyController(
            self.player,
            stop_callback=self.stop_reading,
            exit_callback=self.shutdown,
        )

        self.tray = TrayApp(self)

    def validate_model(self):
        return PIPER_MODEL.exists() and PIPER_CONFIG.exists()

    def on_text_selected(self, text):
        if text:
            self.reader_queue.put(text)

    def stop_reading(self):
        self.reader_queue.clear()
        self.player.stop()

    def toggle_pause(self):
        self.player.pause_resume()

    def speak(self, text):
        try:
            chunks = split_text(text)
            for index, chunk in enumerate(chunks, 1):
                if self.exit_event.is_set():
                    break

                print(f"朗读第 {index}/{len(chunks)} 段")

                audio_file = self.tts.generate(chunk)
                if not audio_file:
                    continue

                self.player.play(audio_file)

                while self.player.is_playing() or self.player.paused:
                    if self.exit_event.is_set():
                        self.player.stop()
                        break
                    time.sleep(0.08)

                try:
                    os.remove(audio_file)
                except OSError:
                    pass

        except Exception as exc:
            print(f"朗读任务异常: {exc}")

    def start(self):
        if not self.validate_model():
            print("缺少 Piper 中文模型文件")
            print(PIPER_MODEL)
            return 1

        print(f"{APP_NAME} V{APP_VERSION} 已启动")

        self.reader_queue.start()
        self.selection_monitor.start()
        self.hotkey.start()
        self.tray.run()

        return 0

    def shutdown(self):
        if self.exit_event.is_set():
            return

        self.exit_event.set()
        self.reader_queue.stop()
        self.selection_monitor.stop()
        self.hotkey.stop()
        self.player.stop()
        self.tray.stop()


def main():
    app = EasyReader()
    return app.start()


if __name__ == "__main__":
    raise SystemExit(main())
