# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #7：4.3 函数式工厂：工厂本身就是一个函数
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Car:
    def drive(self):
        return "汽车出发 🚗"


class Bike:
    def ride(self):
        return "自行车出发 🚲"


def make_car():
    return Car()

def make_bike():
    return Bike()


def deliver(vehicle_factory):
    return vehicle_factory()      # 把工厂函数当参数，需要时再调用


print(deliver(make_car).drive())
print(deliver(make_bike).ride())
