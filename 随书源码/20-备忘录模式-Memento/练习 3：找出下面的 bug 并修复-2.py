# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #12：练习 3：找出下面的 bug 并修复
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
        return copy.deepcopy(self)      # 修复：深拷贝


g = Game()
g.move(0, 0)
snap = g.save()
g.move(1, 1)
print("修复后快照：", snap.level_map)
print("修复后分数：", snap.score)
