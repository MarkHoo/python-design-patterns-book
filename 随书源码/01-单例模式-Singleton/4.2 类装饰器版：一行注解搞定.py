# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #7：4.2 类装饰器版：一行注解搞定
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import functools


def singleton(cls):
    """类装饰器：把任意类变成单例"""
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if wrapper.instance is None:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper


@singleton
class Cache:
    def __init__(self):
        self.data = {}


c1 = Cache()
c2 = Cache()
print("c1 is c2:", c1 is c2)
