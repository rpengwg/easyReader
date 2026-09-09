import threading

from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem


class TrayApp:
    def __init__(self, app):
        self.app = app
        self.icon = None
        self.thread = None

    @staticmethod
    def _image():
        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((8, 8, 56, 56), fill=(40, 110, 220, 255))
        draw.polygon([(25, 28), (35, 20), (35, 44), (25, 36)], fill="white")
        draw.arc((34, 22, 50, 42), start=300, end=60, fill="white", width=3)
        return image

    def _build_icon(self):
        menu = Menu(
            MenuItem("暂停 / 继续", lambda icon, item: self.app.toggle_pause()),
            MenuItem("停止朗读", lambda icon, item: self.app.stop_reading()),
            MenuItem("退出 EasyReader", lambda icon, item: self.app.shutdown()),
        )
        self.icon = Icon("EasyReader", self._image(), "EasyReader V1.0", menu)

    def run(self):
        self._build_icon()
        self.thread = threading.Thread(target=self.icon.run, daemon=True)
        self.thread.start()
        print("EasyReader 正在后台运行，可在系统托盘中控制。")
        while not self.app.exit_event.is_set():
            self.app.exit_event.wait(0.5)

    def stop(self):
        if self.icon:
            try:
                self.icon.stop()
            except Exception:
                pass
