# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：用一堆位置参数构造复杂对象——第 4 个参数是啥来着？
class Computer:
    def __init__(self, cpu, memory, gpu, storage, power, case, os_name, has_wifi):
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu
        self.storage = storage
        self.power = power
        self.case = case
        self.os_name = os_name
        self.has_wifi = has_wifi

# 8 个位置参数，谁还记得第 4 个是硬盘还是电源？
pc = Computer("i7-13700K", 32, "RTX 4070", "1TB SSD", "750W", "中塔机箱", "Windows 11", True)
print(f"组装了一台 {pc.cpu} + {pc.gpu} 的电脑")
