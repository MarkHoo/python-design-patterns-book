# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #10：误区 2：过度设计——俩分支也上策略
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 误区 2：过度设计——只有一两个分支也硬上策略模式
def tax(income: float, is_tech: bool) -> float:
    """只有两种税率，直接 if 就够清晰了"""
    rate = 0.10 if is_tech else 0.20
    return income * rate


print("科技公司：", tax(10000, True))
print("普通公司：", tax(10000, False))
print("（等算法种类多了、需要运行时切换时，再升级成策略模式）")
