# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #7：4.3 无状态状态对象：全局共享也不串
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class StoppedState:
    def play(self, player) -> None:
        player.state = PLAYING
        print("停止 → 播放")

    def pause(self, player) -> None:
        print("已经停止了，无法暂停")

    def stop(self, player) -> None:
        print("已经停止了")


class PlayingState:
    def play(self, player) -> None:
        print("正在播放中")

    def pause(self, player) -> None:
        player.state = PAUSED
        print("播放 → 暂停")

    def stop(self, player) -> None:
        player.state = STOPPED
        print("播放 → 停止")


class PausedState:
    def play(self, player) -> None:
        player.state = PLAYING
        print("暂停 → 播放")

    def pause(self, player) -> None:
        print("已经暂停了")

    def stop(self, player) -> None:
        player.state = STOPPED
        print("暂停 → 停止")


# 无状态的状态对象：全局共享一份，谁用都不串
STOPPED = StoppedState()
PLAYING = PlayingState()
PAUSED = PausedState()


class Player:
    """上下文：持有当前状态，把请求转发给状态对象"""

    def __init__(self):
        self.state = STOPPED

    def play(self) -> None:
        self.state.play(self)

    def pause(self) -> None:
        self.state.pause(self)

    def stop(self) -> None:
        self.state.stop(self)


p1 = Player()
p2 = Player()          # 两个播放器共享同一批状态对象
p1.play()
p1.pause()
p2.play()              # p2 还是 stopped，直接进入播放
print("p1 状态:", type(p1.state).__name__)
print("p2 状态:", type(p2.state).__name__)
