# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #3：3.2 播放器：上下文里转移（另一种风格）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class StoppedState:
    def play(self):
        print("开始播放")
        return PlayingState()

    def pause(self):
        print("已经停止了，无法暂停")
        return self

    def stop(self):
        print("已经停止了")
        return self


class PlayingState:
    def play(self):
        print("正在播放中")
        return self

    def pause(self):
        print("暂停")
        return PausedState()

    def stop(self):
        print("停止")
        return StoppedState()


class PausedState:
    def play(self):
        print("恢复播放")
        return PlayingState()

    def pause(self):
        print("已经暂停了")
        return self

    def stop(self):
        print("停止")
        return StoppedState()


class Player:
    """上下文：只负责'换状态'，不负责'怎么换'"""

    def __init__(self):
        self.state = StoppedState()

    def play(self):
        self.state = self.state.play()

    def pause(self):
        self.state = self.state.pause()

    def stop(self):
        self.state = self.state.stop()


player = Player()
player.play()
player.pause()
player.play()
player.stop()
