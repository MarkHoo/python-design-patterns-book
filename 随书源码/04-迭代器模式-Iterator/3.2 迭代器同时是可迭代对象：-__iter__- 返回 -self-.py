# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #3：3.2 迭代器同时是可迭代对象：`__iter__` 返回 `self`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class CountDown:
    """倒计时迭代器：3 → 1"""

    def __init__(self, start: int):
        self._current = start

    def __iter__(self):
        return self                # 迭代器自己就是可迭代对象

    def __next__(self) -> int:
        if self._current <= 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value


it = CountDown(3)
print("手动取第一个：", next(it))
print("手动取第二个：", next(it))
print("剩下的交给 for：", end=" ")
for n in it:                       # for 会自动捕获 StopIteration
    print(n, end=" ")
print()
