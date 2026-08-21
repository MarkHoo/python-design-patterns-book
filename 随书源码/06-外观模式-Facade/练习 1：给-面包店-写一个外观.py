# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》06-外观模式-Facade
# 代码块 #11：练习 1：给"面包店"写一个外观
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：BakerFacade 把三个子系统串成一条龙
class Mixer:
    def mix(self, ingredient: str) -> None:
        print(f"搅拌 {ingredient}")


class Oven:
    def preheat(self, temp: int) -> None:
        print(f"烤箱预热 {temp} 度")

    def bake(self, minutes: int) -> None:
        print(f"烘烤 {minutes} 分钟")


class Packer:
    def pack(self, product: str) -> None:
        print(f"包装 {product}")


class BakerFacade:
    """面包师外观：从配料到出炉一条龙"""

    def __init__(self):
        self._mixer = Mixer()
        self._oven = Oven()
        self._packer = Packer()

    def make_bread(self, flour: str, temp: int = 180, minutes: int = 30) -> None:
        self._mixer.mix(flour)
        self._oven.preheat(temp)
        self._oven.bake(minutes)
        self._packer.pack("吐司面包")
        print("面包出炉，可以卖了！")


BakerFacade().make_bread("高筋面粉")
