# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #3：3.2 家庭影院：一键观影
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Projector:
    """投影仪"""

    def on(self) -> None:
        print("投影仪：开机")

    def set_mode(self, mode: str) -> None:
        print(f"投影仪：切换到{mode}模式")


class Curtain:
    """窗帘"""

    def close(self) -> None:
        print("窗帘：缓缓拉上")

    def open(self) -> None:
        print("窗帘：拉开")


class SoundSystem:
    """音响"""

    def on(self) -> None:
        print("音响：开机")

    def set_volume(self, level: int) -> None:
        print(f"音响：音量调到 {level}")


class Light:
    """灯光"""

    def dim(self, percent: int) -> None:
        print(f"灯光：调暗到 {percent}%")


class HomeTheaterFacade:
    """家庭影院外观：一键观影、一键散场"""

    def __init__(self):
        self._projector = Projector()
        self._curtain = Curtain()
        self._sound = SoundSystem()
        self._light = Light()

    def watch_movie(self, movie: str) -> None:
        """一键观影：调暗灯光 → 拉窗帘 → 开投影 → 开音响"""
        print(f"===== 开始观影《{movie}》 =====")
        self._light.dim(10)
        self._curtain.close()
        self._projector.on()
        self._projector.set_mode("影院")
        self._sound.on()
        self._sound.set_volume(30)

    def end_movie(self) -> None:
        """一键散场：关音响 → 投影待机 → 拉开窗帘 → 开灯"""
        print("===== 观影结束 =====")
        self._sound.set_volume(0)
        self._projector.set_mode("待机")
        self._curtain.open()
        self._light.dim(100)


theater = HomeTheaterFacade()
theater.watch_movie("流浪地球3")
theater.end_movie()
