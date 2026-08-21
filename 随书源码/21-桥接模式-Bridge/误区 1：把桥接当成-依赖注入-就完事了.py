# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》21-桥接模式-Bridge
# 代码块 #8：误区 1：把桥接当成"依赖注入"就完事了
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 误区：只有一个维度，却硬套桥接
class Report:
    def __init__(self, writer):     # writer 只是依赖注入
        self._writer = writer

    def generate(self) -> None:
        self._writer.write("报表内容")
