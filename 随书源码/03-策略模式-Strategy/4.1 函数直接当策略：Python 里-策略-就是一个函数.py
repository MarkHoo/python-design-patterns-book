# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #5：4.1 函数直接当策略：Python 里"策略"就是一个函数
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def discount_normal(price: float) -> float:
    return price


def discount_vip(price: float) -> float:
    return price * 0.8


def discount_festival(price: float) -> float:
    """双十一全场五折"""
    return price * 0.5


def checkout(price: float, discount_fn) -> float:
    """上下文退化成一行：调用传入的策略函数"""
    return discount_fn(price)


print("普通：", checkout(100, discount_normal))
print("VIP：", checkout(100, discount_vip))
print("双十一：", checkout(100, discount_festival))
print("临时九折：", checkout(100, lambda p: p * 0.9))
