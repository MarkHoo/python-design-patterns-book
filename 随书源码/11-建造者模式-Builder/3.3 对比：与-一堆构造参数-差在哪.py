# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #4：3.3 对比：与"一堆构造参数"差在哪
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Computer:
    """直接构造：位置参数"""

    def __init__(self, cpu, memory, gpu):
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu

    def __repr__(self):
        return f"<电脑 {self.cpu} / 内存{self.memory}G / {self.gpu}>"

class ComputerBuilder:
    """建造者：每个配置项都有名字"""

    def __init__(self):
        self._c = Computer(None, None, None)

    def cpu(self, v):
        self._c.cpu = v
        return self

    def memory(self, v):
        self._c.memory = v
        return self

    def gpu(self, v):
        self._c.gpu = v
        return self

    def build(self):
        return self._c

# 方案 A：位置参数——第 3 个到底是显卡还是内存？顺序错了没人拦
pc_a = Computer("i7-13700K", 32, "RTX 4070")

# 方案 B：建造者——每个配置都有名字，读代码像读配置单
pc_b = (ComputerBuilder()
        .cpu("i7-13700K")
        .memory(32)
        .gpu("RTX 4070")
        .build())

print("方案 A：", pc_a)
print("方案 B：", pc_b)
