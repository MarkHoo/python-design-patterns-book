# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》20-备忘录模式-Memento
# 代码块 #3：3.2 游戏版：存档点恢复角色状态
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Memento:
    hp: int
    level: int
    inventory: list


class Hero:
    """发起人：游戏主角"""

    def __init__(self, name: str):
        self.name = name
        self.hp = 100
        self.level = 1
        self.inventory = ["木剑"]

    def take_damage(self, dmg: int) -> None:
        self.hp = max(0, self.hp - dmg)

    def level_up(self) -> None:
        self.level += 1
        self.hp = min(100, self.hp + 30)

    def pick_item(self, item: str) -> None:
        self.inventory.append(item)

    def save(self) -> Memento:
        return Memento(hp=self.hp, level=self.level, inventory=copy.deepcopy(self.inventory))

    def restore(self, m: Memento) -> None:
        self.hp = m.hp
        self.level = m.level
        self.inventory = copy.deepcopy(m.inventory)

    def __repr__(self):
        return f"{self.name}(HP={self.hp}, Lv.{self.level}, 背包={self.inventory})"


hero = Hero("勇者阿强")
print("出发：", hero)

save_point = hero.save()                  # 进 BOSS 房前存档
hero.take_damage(85)
hero.pick_item("龙鳞")
print("打完 BOSS：", hero)                # 惨胜，还捡了装备

hero.restore(save_point)                  # 等等，太惨了，读档重来！
print("读档后：", hero)                   # 回到满状态，但龙鳞也没了——这就是读档的代价
