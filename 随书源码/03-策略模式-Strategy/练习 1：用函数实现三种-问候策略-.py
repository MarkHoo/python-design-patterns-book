# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #12：练习 1：用函数实现三种"问候策略"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def greet_cn(name: str) -> str:
    return f"你好，{name}！"


def greet_en(name: str) -> str:
    return f"Hello, {name}!"


def greet_fun(name: str) -> str:
    return f"嗨嗨～{name}～(*´▽`*)"


def greet(name: str, strategy) -> str:
    """上下文：调用传入的策略"""
    return strategy(name)


print(greet("小明", greet_cn))
print(greet("小明", greet_en))
print(greet("小明", greet_fun))
