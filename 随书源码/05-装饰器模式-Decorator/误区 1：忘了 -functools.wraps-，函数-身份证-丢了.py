# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #13：误区 1：忘了 `functools.wraps`，函数"身份证"丢了
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def log_bad(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@log_bad
def hello():
    """你好函数"""
    return "你好"


print("函数名变成了：", hello.__name__)   # 应该是 hello，却是 wrapper
print("文档也没了：", hello.__doc__)
