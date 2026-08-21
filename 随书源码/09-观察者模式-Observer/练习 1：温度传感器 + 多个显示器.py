# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #12：练习 1：温度传感器 + 多个显示器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：经典的"一个主题 + 多个观察者"
import abc


class Display(abc.ABC):
    @abc.abstractmethod
    def show(self, temp: float) -> None:
        pass


class Thermostat:
    """温度传感器：被观察者"""

    def __init__(self):
        self._displays = []

    def attach(self, d: Display):
        self._displays.append(d)

    def set_temp(self, temp: float):
        print(f"温度变化：{temp}℃")
        for d in self._displays:
            d.show(temp)


class PhoneDisplay(Display):
    def show(self, temp):
        print(f"  [手机] 当前室温 {temp}℃")


class WallDisplay(Display):
    def show(self, temp):
        print(f"  [挂墙屏] 室温 {temp}℃，建议开空调")


t = Thermostat()
t.attach(PhoneDisplay())
t.attach(WallDisplay())
t.set_temp(26.0)
t.set_temp(31.5)
