# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #10：误区 1：状态模式与策略模式混淆
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class NormalState:
    def attack(self, hero) -> None:
        print("普通攻击，伤害 10")
        if hero.rage >= 80:
            hero.state = RageState()
            print("怒气爆发！进入狂暴状态")


class RageState:
    def attack(self, hero) -> None:
        print("狂暴攻击，伤害 50！")


class Hero:
    def __init__(self):
        self.rage = 0
        self.state = NormalState()

    def attack(self) -> None:
        self.state.attack(self)

    def gain_rage(self, amount: int) -> None:
        self.rage += amount


hero = Hero()
hero.gain_rage(30)
hero.attack()
hero.gain_rage(60)
hero.attack()        # 这次攻击后怒气 90，触发狂暴
hero.attack()        # 已经是狂暴攻击
print("当前状态:", type(hero.state).__name__)
