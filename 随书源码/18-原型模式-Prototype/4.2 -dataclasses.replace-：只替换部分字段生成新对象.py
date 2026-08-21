# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #6：4.2 `dataclasses.replace`：只替换部分字段生成新对象
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from dataclasses import dataclass, replace


@dataclass
class Weapon:
    name: str
    damage: int


@dataclass
class Soldier:
    name: str
    hp: int
    weapon: Weapon


s1 = Soldier("小强", 100, Weapon("步枪", 30))

# replace 只替换指定字段，其余字段原样复制——天然的原型操作
s2 = replace(s1, name="阿伟")
s3 = replace(s1, hp=150, weapon=Weapon("狙击枪", 90))

print(s1)
print(s2)
print(s3)

# 注意：replace 是"浅"的——没替换的 weapon 还是同一个对象
s2.weapon.damage = 999
print("改 s2 的武器，原版也遭殃：", s1.weapon.damage)
