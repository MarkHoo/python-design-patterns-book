# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #5：3.4 元类版：从"源头"上禁止重复创建
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class SingletonMeta(type):
    """元类版单例：所有用这个元类的类自动成为单例"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:              # 这个类还没有实例？
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    def __init__(self, name: str = "default"):
        print(f"初始化 Logger：{name}")   # 注意：只打印一次
        self.name = name


l1 = Logger("app")
l2 = Logger("app")
l3 = Logger("other")
print("l1 is l2:", l1 is l2)
print("l1 is l3:", l1 is l3, "（第二次传参被忽略，name 仍是第一次的）")
