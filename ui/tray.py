from pystray import Icon, MenuItem, Menu
from PIL import Image


def start_tray(player, stop_callback):
    image = Image.new("RGB", (64, 64), "black")

    menu = Menu(
        MenuItem("暂停/继续", lambda: player.pause_resume()),
        MenuItem("停止", lambda: player.stop()),
        MenuItem("退出", lambda: stop_callback()),
    )

    icon = Icon("EasyReader", image, "EasyReader", menu)
    icon.run()
