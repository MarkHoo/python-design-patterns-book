# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #8：4.2 用类实现装饰器：`__call__`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import functools


class CountCalls:
    """类装饰器：统计函数被调用了多少次"""

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        print(f"第 {self.calls} 次调用 {self.func.__name__}")
        return self.func(*args, **kwargs)


@CountCalls
def ping():
    return "pong"


print(ping())
print(ping())
print(ping())
