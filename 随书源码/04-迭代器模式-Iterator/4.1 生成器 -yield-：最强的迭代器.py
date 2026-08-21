# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #5：4.1 生成器 `yield`：最强的迭代器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def countdown(n: int):
    while n > 0:
        yield n
        n -= 1


def even_numbers(limit: int):
    """生成偶数序列"""
    for i in range(limit):
        if i % 2 == 0:
            yield i


print("倒计时：", list(countdown(5)))
print("前几个偶数：", list(even_numbers(10)))
