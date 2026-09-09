import threading
import time

from pynput import mouse

from config import MAX_TEXT_LENGTH, MIN_TEXT_LENGTH, SELECTION_DELAY
from capture.auto_copy import copy_selection


class SelectionMonitor:
    def __init__(self, callback):
        self.callback = callback
        self.listener = None
        self.mouse_pressed = False
        self.last_text = ""
        self._lock = threading.Lock()

    def on_click(self, x, y, button, pressed):
        if button != mouse.Button.left:
            return
        if pressed:
            self.mouse_pressed = True
            return
        if not self.mouse_pressed:
            return
        self.mouse_pressed = False
        threading.Thread(target=self.handle_selection, daemon=True).start()

    def handle_selection(self):
        time.sleep(SELECTION_DELAY)
        if not self._lock.acquire(blocking=False):
            return
        try:
            text = self.get_selected_text()
            if not text:
                text = copy_selection()
            if not text:
                return
            text = " ".join(text.split())
            if len(text) < MIN_TEXT_LENGTH or len(text) > MAX_TEXT_LENGTH:
                return
            if text == self.last_text:
                return
            self.last_text = text
            print(f"检测到选中文字：{text[:120]}")
            self.callback(text)
        except Exception as exc:
            print(f"读取选中文字失败：{exc}")
        finally:
            self._lock.release()

    def get_selected_text(self):
        """Best-effort Windows UI Automation selection retrieval."""
        try:
            import uiautomation as auto
            control = auto.GetFocusedControl()
            if not control:
                return None
            try:
                pattern = control.GetSelectionPattern()
                items = pattern.GetSelection()
                values = [item.Name for item in items if getattr(item, "Name", "")]
                if values:
                    return " ".join(values)
            except Exception:
                pass
        except Exception:
            pass
        return None

    def start(self):
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()
        print("鼠标选中文本监听已启动")

    def stop(self):
        if self.listener:
            self.listener.stop()
