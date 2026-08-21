# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #14：练习 3：用原型注册表批量刷怪
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class Monster:
    def __init__(self, name, hp, drops):
        self.name = name
        self.hp = hp
        self.drops = drops
    def clone(self):
        return copy.deepcopy(self)
    def __repr__(self):
        return f"{self.name}(hp={self.hp}) 掉落:{self.drops}"


registry = {
    "史莱姆": Monster("史莱姆", 30, ["黏液"]),
    "哥布林": Monster("哥布林", 60, ["短剑"]),
}

for kind in ("史莱姆", "哥布林"):
    for i in range(3):
        m = registry[kind].clone()
        m.hp += i * 5
        print(f"{kind} 第{i + 1}只：{m}")
