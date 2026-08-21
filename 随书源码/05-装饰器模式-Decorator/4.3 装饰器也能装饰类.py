# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #9：4.3 装饰器也能装饰类
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def add_repr(cls):
    """类装饰器：自动生成 __repr__（列出所有实例属性）"""
    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls


@add_repr
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


u = User("小明", 18)
print(u)               # 没写 __repr__，但装饰器给补上了
