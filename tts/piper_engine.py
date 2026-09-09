import os
import subprocess
import threading

from config import (
    PIPER_MODEL,
    AUDIO_FILE,
    TEMP_DIR
)


class PiperEngine:


    def __init__(self):

        self.lock = threading.Lock()


        if not os.path.exists(
            TEMP_DIR
        ):

            os.makedirs(
                TEMP_DIR
            )


    def generate(
        self,
        text
    ):

        """
        将文字转换为 WAV
        """

        with self.lock:

            try:

                # 删除旧文件
                if os.path.exists(
                    AUDIO_FILE
                ):

                    os.remove(
                        AUDIO_FILE
                    )


                command = [

                    "piper",

                    "--model",

                    PIPER_MODEL,

                    "--output_file",

                    AUDIO_FILE

                ]


                process = subprocess.run(

                    command,

                    input=text,

                    text=True,

                    encoding="utf-8",

                    capture_output=True

                )


                if process.returncode != 0:

                    print(
                        "Piper 错误："
                    )

                    print(
                        process.stderr
                    )

                    return None


                if os.path.exists(
                    AUDIO_FILE
                ):

                    return AUDIO_FILE


            except Exception as e:

                print(
                    "生成语音失败：",
                    e
                )


        return None
