from pynput import keyboard


class HotkeyController:
    def __init__(self, player, stop_callback=None, exit_callback=None):
        self.player = player
        self.stop_callback = stop_callback
        self.exit_callback = exit_callback
        self.listener = None
        self.ctrl_pressed = False
        self.shift_pressed = False

    def on_press(self, key):
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            self.ctrl_pressed = True
        elif key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
            self.shift_pressed = True
        elif key == keyboard.Key.esc:
            if self.ctrl_pressed:
                if self.stop_callback:
                    self.stop_callback()
            else:
                self.player.pause_resume()
        elif hasattr(key, "char") and key.char and key.char.lower() == "e":
            if self.ctrl_pressed and self.shift_pressed and self.exit_callback:
                self.exit_callback()

    def on_release(self, key):
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            self.ctrl_pressed = False
        elif key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
            self.shift_pressed = False

    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        print("快捷键已启动：ESC 暂停/继续，Ctrl+ESC 停止，Ctrl+Shift+E 退出")

    def stop(self):
        if self.listener:
            self.listener.stop()
