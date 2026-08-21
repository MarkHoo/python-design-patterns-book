# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #4：3.3 无限序列：斐波那契迭代器（惰性求值）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Fibonacci:
    """无限斐波那契数列的迭代器"""

    def __init__(self):
        self._a, self._b = 0, 1

    def __iter__(self):
        return self

    def __next__(self) -> int:
        value = self._a
        self._a, self._b = self._b, self._a + self._b
        return value


fib = Fibonacci()
first_ten = [next(fib) for _ in range(10)]
print("前 10 个斐波那契数：", first_ten)
