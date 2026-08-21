# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》08-模板方法-Template-Method
# 代码块 #3：3.2 变体：游戏关卡
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import abc


class GameLevel(abc.ABC):
    """抽象关卡：开局 → 打怪 → 结算 的骨架固定"""

    def play(self) -> None:
        """模板方法：整关的流程，子类不能改"""
        self.on_start()
        self.spawn_enemies()
        self.battle()
        self.on_clear()
        if self.bonus_round():            # 钩子：默认没有奖励关
            self.play_bonus()

    def on_start(self) -> None:
        print("关卡开始，加载地图……")

    @abc.abstractmethod
    def spawn_enemies(self) -> None:
        pass

    @abc.abstractmethod
    def battle(self) -> None:
        pass

    def on_clear(self) -> None:
        print("敌人清空，本关通过！")

    def bonus_round(self) -> bool:
        """钩子：默认没有奖励关"""
        return False

    def play_bonus(self) -> None:
        print("进入奖励关！")


class ForestLevel(GameLevel):
    def spawn_enemies(self) -> None:
        print("出现 5 只史莱姆")

    def battle(self) -> None:
        print("主角挥剑，击败史莱姆")


class BossLevel(GameLevel):
    def spawn_enemies(self) -> None:
        print("出现最终 Boss：暗影魔王")

    def battle(self) -> None:
        print("Boss 战！消耗三个血瓶险胜")

    def bonus_round(self) -> bool:
        return True   # 覆盖钩子：Boss 关有奖励关

    def play_bonus(self) -> None:
        print("奖励关：连开三个宝箱！")


print("===== 第 1 关 =====")
ForestLevel().play()
print("===== 最终关 =====")
BossLevel().play()
