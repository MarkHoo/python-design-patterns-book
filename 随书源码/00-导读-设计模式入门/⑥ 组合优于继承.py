# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》00-导读-设计模式入门
# 代码块 #9：⑥ 组合优于继承
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Engine:
    def start(self) -> str:
        return "引擎轰鸣 🚗"


class Wheels:
    def roll(self) -> str:
        return "车轮滚动"


# 反面教材：继承狂魔
class Vehicle:
    pass


class Car(Vehicle):
    pass


class GasCar(Car):
    pass


class GasCarWithNitro(GasCar):   # 这种类爆炸你怕不怕
    pass


# 正确姿势：组合
class Car:
    def __init__(self):
        self.engine = Engine()    # 车"有一个"引擎
        self.wheels = Wheels()    # 车"有一个"轮子

    def drive(self) -> str:
        return f"{self.engine.start()}，{self.wheels.roll()}"


print(Car().drive())
