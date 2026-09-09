import pygame
import threading


class AudioPlayer:


    def __init__(self):

        pygame.mixer.init()

        self.paused = False

        self.lock = threading.Lock()


    def play(
        self,
        audio_file
    ):

        with self.lock:

            # 停止之前的播放
            pygame.mixer.music.stop()


            pygame.mixer.music.load(
                audio_file
            )


            pygame.mixer.music.play()


            self.paused = False


            print(
                "▶ 开始朗读"
            )


    def pause_resume(self):

        with self.lock:

            if pygame.mixer.music.get_busy():

                if not self.paused:

                    pygame.mixer.music.pause()

                    self.paused = True

                    print(
                        "⏸ 已暂停"
                    )


                else:

                    pygame.mixer.music.unpause()

                    self.paused = False

                    print(
                        "▶ 继续播放"
                    )


    def stop(self):

        with self.lock:

            pygame.mixer.music.stop()

            self.paused = False

            print(
                "■ 停止朗读"
            )


    def is_playing(self):

        return pygame.mixer.music.get_busy()
