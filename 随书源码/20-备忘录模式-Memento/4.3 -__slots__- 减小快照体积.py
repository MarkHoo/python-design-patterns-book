# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #7：4.3 `__slots__` 减小快照体积
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy
from dataclasses import dataclass


@dataclass
class Frame:
    """游戏帧快照：__slots__ 让实例更轻量"""
    __slots__ = ("x", "y", "hp")
    x: float
    y: float
    hp: int


f = Frame(10.0, 20.0, 100)
snap = copy.deepcopy(f)
print("快照成功：", snap)
print("实例没有 __dict__（更省内存）：", not hasattr(f, "__dict__"))
