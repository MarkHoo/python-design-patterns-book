# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #8：误区 1：浅拷贝当深拷贝，快照"名存实亡"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class Cart:
    def __init__(self):
        self.items = []

    def add(self, item: str) -> None:
        self.items.append(item)

    def snapshot(self):
        return copy.copy(self)          # 误区：浅拷贝！items 还是同一个列表


cart = Cart()
cart.add("苹果")
snap = cart.snapshot()
cart.add("香蕉")                        # 原对象改了
print("快照里的 items：", snap.items)    # 浅拷贝共享列表 → 快照也"看到"了香蕉
