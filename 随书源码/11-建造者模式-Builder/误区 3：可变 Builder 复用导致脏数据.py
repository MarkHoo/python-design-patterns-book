# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #9：误区 3：可变 Builder 复用导致脏数据
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class DirtyBuilder:
    """反面教材：build 后不重置，复用会串数据"""

    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)
        return self

    def build(self):
        return self.parts    # 直接把内部列表交出去

b = DirtyBuilder()
first = b.add("CPU").add("内存").build()
second = b.add("显卡").build()          # 复用同一个 builder
print("第一个：", first)
print("第二个：", second)
