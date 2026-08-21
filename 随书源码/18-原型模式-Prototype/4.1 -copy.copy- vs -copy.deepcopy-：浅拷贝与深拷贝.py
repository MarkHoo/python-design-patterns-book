# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #5：4.1 `copy.copy` vs `copy.deepcopy`：浅拷贝与深拷贝
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class Skill:
    def __init__(self, name, level):
        self.name = name
        self.level = level
    def __repr__(self):
        return f"Skill({self.name}, Lv{self.level})"


class Character:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills


hero = Character("勇者", [Skill("斩击", 3), Skill("火球", 2)])

shallow = copy.copy(hero)      # 浅拷贝：只复制外壳
deep = copy.deepcopy(hero)     # 深拷贝：连内部对象一起复制

print("浅拷贝共享技能列表：", shallow.skills is hero.skills)   # True
print("深拷贝技能列表独立：", deep.skills is hero.skills)      # False

# 修改浅拷贝里的技能等级，原版跟着变——经典 bug！
shallow.skills[0].level = 9
print("原版技能等级：", [s.level for s in hero.skills])    # 被改成了 9
print("深拷贝技能等级：", [s.level for s in deep.skills])   # 还是 3
