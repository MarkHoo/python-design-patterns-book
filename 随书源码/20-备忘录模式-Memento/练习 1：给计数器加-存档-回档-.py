# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #9：练习 1：给计数器加"存档/回档"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class Counter:
    def __init__(self):
        self.count = 0
        self.history = []

    def inc(self, n: int = 1) -> None:
        self.count += n

    def save(self):
        return copy.deepcopy(self.count)

    def restore(self, snap) -> None:
        self.count = copy.deepcopy(snap)


c = Counter()
c.inc(3)
c.inc(4)
snap = c.save()          # 存档：count=7
c.inc(100)
print("加过头了：", c.count)
c.restore(snap)
print("读档后：", c.count)
