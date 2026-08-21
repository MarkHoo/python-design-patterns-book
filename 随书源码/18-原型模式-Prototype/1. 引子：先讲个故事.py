# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有原型的世界——每次复制对象都手写一遍字段
class Soldier:
    def __init__(self, name, hp, weapons):
        self.name = name
        self.hp = hp
        self.weapons = weapons  # 武器列表


s1 = Soldier("列兵小强", 100, ["步枪", "手雷"])

# 复制一个士兵：手动 new + 手工抄字段（抄着抄着就漏了）
s2 = Soldier(s1.name, s1.hp, s1.weapons)

# 更糟的是：s2 和 s1 的 weapons 是同一个列表！
s2.weapons.append("急救包")
print("原版的武器：", s1.weapons)
print("复制品的武器：", s2.weapons)
