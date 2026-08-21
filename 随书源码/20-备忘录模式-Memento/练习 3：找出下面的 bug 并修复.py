# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #11：练习 3：找出下面的 bug 并修复
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class Game:
    def __init__(self):
        self.level_map = [[0] * 3 for _ in range(3)]
        self.score = 0

    def move(self, x: int, y: int) -> None:
        self.level_map[x][y] = 1
        self.score += 10

    def save(self):
        # bug：浅拷贝！level_map 的嵌套列表还是共享的
        return copy.copy(self)


g = Game()
g.move(0, 0)
snap = g.save()
g.move(1, 1)          # 原游戏继续走
print("看，快照里的 (1,1) 也被踩了：", snap.level_map)
