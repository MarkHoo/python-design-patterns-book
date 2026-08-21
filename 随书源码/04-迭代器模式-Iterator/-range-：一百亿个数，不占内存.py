# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #10：`range`：一百亿个数，不占内存
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

r = range(10**10)                  # 一百亿个数，但不占内存
print("range 对象：", r)
print("前 5 个：", list(r[:5]))
print("前 100 个之和：", sum(range(100)))
