# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #15：练习 3：把 if/elif 播放器改成状态模式
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：状态模式重写播放器（无状态单例状态对象）
class Stopped:
    def play(self, p) -> None:
        p.state = Playing()
        print("停止 → 播放")

    def stop(self, p) -> None:
        print("已经停止了")


class Playing:
    def play(self, p) -> None:
        print("正在播放中")

    def stop(self, p) -> None:
        p.state = Stopped()
        print("播放 → 停止")


class Player:
    def __init__(self):
        self.state = Stopped()

    def play(self) -> None:
        self.state.play(self)

    def stop(self) -> None:
        self.state.stop(self)


p = Player()
p.play()
p.stop()
p.stop()
