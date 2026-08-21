# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #7：4.1 `functools.wraps`：保住函数的"身份证"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import functools


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@log
def hello():
    """我是 hello 函数的文档"""
    return "你好"


print("函数名：", hello.__name__)
print("文档：", hello.__doc__)
