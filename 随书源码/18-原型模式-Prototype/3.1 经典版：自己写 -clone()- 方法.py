# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #2：3.1 经典版：自己写 `clone()` 方法
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy


class Enemy:
    """经典原型：敌人单位，clone() 返回一份独立拷贝"""
    def __init__(self, kind, hp, skills):
        self.kind = kind
        self.hp = hp
        self.skills = skills  # 技能列表（嵌套结构）
    def clone(self):
        # 新建同类型对象，deepcopy 复制 skills，避免两份共享列表
        return Enemy(self.kind, self.hp, copy.deepcopy(self.skills))
    def __repr__(self):
        return f"<Enemy {self.kind} hp={self.hp} skills={self.skills}>"


zombie = Enemy("僵尸", 50, ["撕咬", "感染"])
zombie2 = zombie.clone()

zombie2.hp = 80              # 给复制品加血量
zombie2.skills.append("自爆")  # 给复制品加技能

print("原版：", zombie)
print("复制品：", zombie2)
print("互不影响：", zombie.skills == ["撕咬", "感染"])
