# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #13：练习 2：补全一个能换策略的 `Sorter`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Sorter:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy(data)


def asc(data):
    return sorted(data)


def desc(data):
    return sorted(data, reverse=True)

sorter = Sorter(asc)
print("升序：", sorter.sort([3, 1, 2]))
sorter.set_strategy(desc)
print("降序：", sorter.sort([3, 1, 2]))
