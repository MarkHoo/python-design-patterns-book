# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #9：误区 1：状态模式与策略模式混淆
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class SwordAttack:
    def attack(self) -> str:
        return "挥剑攻击，伤害 30"


class BowAttack:
    def attack(self) -> str:
        return "拉弓射击，伤害 20"


class Hero:
    def __init__(self, weapon):
        self.weapon = weapon          # 策略：随时可换

    def set_weapon(self, weapon) -> None:
        self.weapon = weapon

    def attack(self) -> str:
        return self.weapon.attack()


hero = Hero(SwordAttack())
print("用剑:", hero.attack())
hero.set_weapon(BowAttack())
print("换弓:", hero.attack())
print("换成弓之后，角色还是原来的角色（状态没变）")
