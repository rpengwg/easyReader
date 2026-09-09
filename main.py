import time
import threading

from capture.selection import SelectionMonitor
from tts.piper_engine import PiperEngine
from tts.player import AudioPlayer
from tts.splitter import split_text
from control.hotkey import HotkeyController


class EasyReader:
    def __init__(self):
        self.tts = PiperEngine()
        self.player = AudioPlayer()
        self.selection_monitor = SelectionMonitor(callback=self.on_text_selected)
        self.hotkey = HotkeyController(player=self.player)
        self.processing = False
        self.stop_event = threading.Event()

    def on_text_selected(self, text):
        self.stop_event.set()
        self.player.stop()
        threading.Thread(target=self.speak, args=(text,), daemon=True).start()

    def speak(self, text):
        self.processing = True
        self.stop_event.clear()
        try:
            chunks = split_text(text)
            for index, chunk in enumerate(chunks, 1):
                if self.stop_event.is_set():
                    break
                print(f"正在生成第 {index}/{len(chunks)} 段语音...")
                audio_file = self.tts.generate(chunk)
                if not audio_file:
                    continue
                self.player.play(audio_file)
                while self.player.is_playing() or self.player.paused:
                    if self.stop_event.is_set():
                        self.player.stop()
                        break
                    time.sleep(0.1)
        except Exception as e:
            print("朗读错误：", e)
        finally:
            self.processing = False

    def start(self):
        print("=" * 50)
        print("EasyReader V1.0 启动")
        print("鼠标选择文字 → 自动朗读")
        print("ESC → 暂停 / 继续")
        print("=" * 50)
        self.selection_monitor.start()
        self.hotkey.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("正在退出...")
        finally:
            self.stop_event.set()
            self.selection_monitor.stop()
            self.hotkey.stop()
            self.player.stop()


if __name__ == "__main__":
    EasyReader().start()
