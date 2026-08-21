# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #4：3.3 原型注册表：按名字批量克隆
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class Boss:
    """Boss 原型"""
    def __init__(self, name, hp, skill):
        self.name = name
        self.hp = hp
        self.skill = skill
    def clone(self):
        return copy.deepcopy(self)
    def __repr__(self):
        return f"<Boss {self.name} hp={self.hp} skill={self.skill}>"


class PrototypeRegistry:
    """原型注册表：登记好各种原型，按名字取用克隆"""
    def __init__(self):
        self._prototypes = {}
    def register(self, name, prototype):
        self._prototypes[name] = prototype
    def create(self, name):
        """按名字克隆出一个新对象"""
        if name not in self._prototypes:
            raise KeyError(f"没有登记叫 {name} 的原型")
        return self._prototypes[name].clone()


registry = PrototypeRegistry()
registry.register("史莱姆王", Boss("史莱姆王", 500, "分裂"))
registry.register("骷髅王", Boss("骷髅王", 800, "召唤骷髅"))
registry.register("最终魔王", Boss("最终魔王", 3000, "灭世一击"))

# 打副本：同一关要刷 3 只骷髅王（每只独立，血量微调）
for i in range(3):
    sk = registry.create("骷髅王")
    sk.hp += i * 50
    print(f"第 {i + 1} 只：{sk}")
