# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #10：误区 1：把适配器和外观搞混
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 适配器：改接口——老温度计说华氏，适配后说摄氏
class OldThermometer:
    def read_fahrenheit(self):
        return 98.6

class TempAdapter:
    def __init__(self, old):
        self._old = old

    def read_celsius(self):
        return (self._old.read_fahrenheit() - 32) * 5 / 9

adapter = TempAdapter(OldThermometer())
print("适配器改了接口：", f"{adapter.read_celsius():.1f} ℃")

# 外观：简化接口——把一大堆操作合成一个"一键离家"
class Light:
    def turn_off(self):
        print("灯已关")

class AirConditioner:
    def turn_off(self):
        print("空调已关")

class Door:
    def lock(self):
        print("门已锁")

class HomeFacade:
    """外观：把 3 个操作打包成 1 个"""

    def __init__(self):
        self.light = Light()
        self.ac = AirConditioner()
        self.door = Door()

    def leave_home(self):
        self.light.turn_off()
        self.ac.turn_off()
        self.door.lock()

HomeFacade().leave_home()
