# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #10：误区 1：以为 `__init__` 只执行一次
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print("__init__ 又被调用了一次！")


s1 = Singleton()
s2 = Singleton()
