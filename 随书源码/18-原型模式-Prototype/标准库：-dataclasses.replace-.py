# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #9：标准库：`dataclasses.replace`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class Unit:
    def __init__(self, name, buffs):
        self.name = name
        self.buffs = buffs


def apply_buff(unit, buff_name):
    new_unit = copy.deepcopy(unit)
    new_unit.buffs.append(buff_name)
    return new_unit


u = Unit("剑士", ["攻击+1"])
u2 = apply_buff(u, "暴击+5")
print("原单位 buff：", u.buffs)
print("新单位 buff：", u2.buffs)
