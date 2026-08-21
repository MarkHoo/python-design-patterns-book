# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #6：3.4 叠加顺序：从下往上包装，从外到内执行
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def layer_a(func):
    def wrapper(*args, **kwargs):
        print("进入 A（最外层）")
        result = func(*args, **kwargs)
        print("离开 A（最外层）")
        return result
    return wrapper


def layer_b(func):
    def wrapper(*args, **kwargs):
        print("进入 B")
        result = func(*args, **kwargs)
        print("离开 B")
        return result
    return wrapper


@layer_a
@layer_b
def core():
    print("核心业务执行中")


core()
