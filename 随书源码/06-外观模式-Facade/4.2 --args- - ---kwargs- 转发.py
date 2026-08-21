# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #6：4.2 `*args` / `**kwargs` 转发
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class CoffeeMachine:
    """咖啡机子系统：一堆可选项"""

    def make(self, beans="阿拉比卡", grind=3, milk="全脂", sugar=0, size="中杯"):
        parts = [f"{size}咖啡", beans, f"研磨度{grind}"]
        if milk:
            parts.append(f"{milk}奶")   # milk 传"全脂"→"全脂奶"，传"燕麦"→"燕麦奶"
        if sugar:
            parts.append(f"{sugar}块糖")
        print("制作：", "、".join(parts))


class BaristaFacade:
    """咖啡师外观：顾客点什么，就原样转达给机器"""

    def __init__(self):
        self._machine = CoffeeMachine()

    def order(self, *args, **kwargs):
        """外观不拆解参数，原样转发给子系统"""
        self._machine.make(*args, **kwargs)


barista = BaristaFacade()
barista.order()                                    # 什么都不说：默认一杯
barista.order(beans="云南小粒", size="大杯")        # 只改部分参数
barista.order("瑰夏", 5, milk="燕麦", sugar=1)      # 位置参数 + 关键字参数混用
