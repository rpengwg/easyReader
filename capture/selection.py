import time
import threading

from pynput import mouse

from config import (
    SELECTION_DELAY,
    MIN_TEXT_LENGTH
)


class SelectionMonitor:

    def __init__(self, callback):

        self.callback = callback

        self.mouse_pressed = False

        self.listener = None

        self.last_text = ""


    def on_click(
        self,
        x,
        y,
        button,
        pressed
    ):

        # 左键按下
        if button == mouse.Button.left:

            if pressed:

                self.mouse_pressed = True

            else:

                # 鼠标左键释放
                if self.mouse_pressed:

                    self.mouse_pressed = False

                    threading.Thread(
                        target=self.handle_selection,
                        daemon=True
                    ).start()


    def handle_selection(self):

        time.sleep(
            SELECTION_DELAY
        )

        text = self.get_selected_text()

        if not text:
            return

        text = text.strip()

        if len(text) < MIN_TEXT_LENGTH:
            return

        # 避免重复朗读
        if text == self.last_text:
            return

        self.last_text = text

        print(
            f"\n检测到文字：\n{text}\n"
        )

        self.callback(text)


    def get_selected_text(self):

        """
        第一版：
        尝试通过 Windows UI Automation
        获取当前控件中的选择文本。
        """

        try:

            import uiautomation as auto


            control = auto.GetFocusedControl()


            if not control:
                return None


            # 尝试获取文本选择模式
            try:

                pattern = (
                    control.GetSelectionPattern()
                )


                selection = (
                    pattern.GetSelection()
                )


                texts = []

                for item in selection:

                    try:

                        texts.append(
                            item.Name
                        )

                    except Exception:
                        pass


                if texts:

                    return " ".join(texts)


            except Exception:
                pass


            # 尝试 ValuePattern
            try:

                value_pattern = (
                    control.GetValuePattern()
                )


                value = (
                    value_pattern.Value
                )


                if value:

                    return value


            except Exception:
                pass


        except Exception as e:

            print(
                "读取选中文字失败：",
                e
            )


        return None


    def start(self):

        print(
            "鼠标文字监听已启动"
        )

        self.listener = mouse.Listener(

            on_click=self.on_click

        )

        self.listener.start()


    def stop(self):

        if self.listener:

            self.listener.stop()
