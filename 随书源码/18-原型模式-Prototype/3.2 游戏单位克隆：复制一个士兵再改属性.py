# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #3：3.2 游戏单位克隆：复制一个士兵再改属性
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class Unit:
    """游戏单位：克隆原型 + 改属性 = 快速造兵"""
    def __init__(self, name, hp, attack, buffs):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.buffs = buffs  # 身上挂的 buff 列表
    def clone(self):
        return copy.deepcopy(self)
    def __repr__(self):
        return f"<Unit {self.name} hp={self.hp} atk={self.attack} buffs={self.buffs}>"


# 先造一个"标准步兵"作为原型
infantry_prototype = Unit("步兵", 100, 10, ["士气+1"])

a = infantry_prototype.clone()
a.name = "精英步兵"
a.attack = 15

b = infantry_prototype.clone()
b.hp = 120

c = infantry_prototype.clone()

print(a)
print(b)
print(c)
print("三份互不影响（buff 列表各自独立）:", a.buffs is not b.buffs and b.buffs is not c.buffs)
