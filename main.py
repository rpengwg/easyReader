import time
import threading

from capture.selection import (
    SelectionMonitor
)

from tts.piper_engine import (
    PiperEngine
)

from tts.player import (
    AudioPlayer
)

from control.hotkey import (
    HotkeyController
)


class EasyReader:


    def __init__(self):

        self.tts = PiperEngine()

        self.player = AudioPlayer()

        self.selection_monitor = (
            SelectionMonitor(

                callback=self.on_text_selected

            )
        )

        self.hotkey = HotkeyController(

            player=self.player

        )


        self.processing = False


    def on_text_selected(
        self,
        text
    ):

        if self.processing:

            return


        threading.Thread(

            target=self.speak,

            args=(text,),

            daemon=True

        ).start()


    def speak(
        self,
        text
    ):

        self.processing = True


        try:

            print(
                "\n正在生成语音..."
            )


            # 停止当前播放
            self.player.stop()


            audio_file = (

                self.tts.generate(
                    text
                )

            )


            if audio_file:

                self.player.play(
                    audio_file
                )

            else:

                print(
                    "语音生成失败"
                )


        except Exception as e:

            print(
                "朗读错误：",
                e
            )


        finally:

            self.processing = False


    def start(self):

        print("=" * 50)

        print(
            "EasyReader 启动"
        )

        print(
            "功能："
        )

        print(
            "鼠标选择文字 → 自动朗读"
        )

        print(
            "ESC → 暂停 / 继续"
        )

        print("=" * 50)


        self.selection_monitor.start()


        self.hotkey.start()


        try:

            while True:

                time.sleep(1)


        except KeyboardInterrupt:

            print(
                "\n正在退出..."
            )


            self.selection_monitor.stop()

            self.hotkey.stop()

            self.player.stop()


if __name__ == "__main__":

    app = EasyReader()

    app.start()
