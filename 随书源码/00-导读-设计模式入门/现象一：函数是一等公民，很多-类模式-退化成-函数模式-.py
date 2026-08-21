# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》00-导读-设计模式入门
# 代码块 #10：现象一：函数是一等公民，很多"类模式"退化成"函数模式"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# Java 风格：策略需要类和接口；Python 风格：直接传函数
def discount_vip(price: float) -> float:
    return price * 0.8


def discount_normal(price: float) -> float:
    return price * 0.95


def checkout(price: float, discount) -> float:
    return discount(price)


print(checkout(100, discount_vip))      # 把函数当参数传
print(checkout(100, discount_normal))
