# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #4：3.3 游戏角色：同一按键，三种行为
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class NormalState:
    """正常：普通攻击，怒气够了自动狂暴"""

    def attack(self, hero) -> None:
        print("普通攻击，伤害 10")
        if hero.rage >= 80:
            hero.state = RageState()
            print("怒气爆发！进入狂暴状态")


class RageState:
    """狂暴：攻击力翻五倍"""

    def attack(self, hero) -> None:
        print("狂暴攻击，伤害 50！")


class DizzyState:
    """眩晕：按键无效"""

    def attack(self, hero) -> None:
        print("角色还在眩晕，攻击键没反应……")


class Hero:
    """上下文：角色"""

    def __init__(self):
        self.rage = 0
        self.state = NormalState()

    def attack(self) -> None:
        self.state.attack(self)

    def gain_rage(self, amount: int) -> None:
        self.rage += amount


hero = Hero()
hero.gain_rage(30)
hero.attack()            # 正常攻击
hero.gain_rage(60)       # 怒气 90 了
hero.attack()            # 这次攻击后触发狂暴
hero.attack()            # 已经是狂暴攻击
hero.state = DizzyState()   # 被 BOSS 打晕
hero.attack()            # 眩晕中，按键无效
