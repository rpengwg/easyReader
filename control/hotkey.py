from pynput import keyboard


class HotkeyController:


    def __init__(
        self,
        player
    ):

        self.player = player

        self.listener = None


    def on_press(
        self,
        key
    ):

        try:

            if key == keyboard.Key.esc:

                self.player.pause_resume()


        except Exception as e:

            print(
                "快捷键错误：",
                e
            )


    def start(self):

        self.listener = keyboard.Listener(

            on_press=self.on_press

        )

        self.listener.start()

        print(
            "ESC 控制已启动"
        )


    def stop(self):

        if self.listener:

            self.listener.stop()
