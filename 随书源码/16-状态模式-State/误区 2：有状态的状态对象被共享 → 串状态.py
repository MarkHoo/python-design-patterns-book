# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #11：误区 2：有状态的状态对象被共享 → 串状态
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：状态对象带着自己的数据，还被全局共享 → 串状态
class PlayingState:
    def __init__(self):
        self.started_at = "未知"      # 状态对象私藏数据

    def play(self, player) -> None:
        self.started_at = f"{player.name} 开始播放的时间"
        print(f"{player.name} 开始播放")

    def describe(self) -> str:
        return self.started_at


PLAYING = PlayingState()      # 全局共享同一个状态对象


class Player:
    def __init__(self, name: str):
        self.name = name
        self.state = PLAYING


p1 = Player("播放器A")
p2 = Player("播放器B")
p1.state.play(p1)
p2.state.play(p2)             # B 覆盖了 A 的记录
print("A 的播放记录被污染:", p1.state.describe())
