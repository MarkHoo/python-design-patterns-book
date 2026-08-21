# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #14：误区 3：包装函数忘了透传参数
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def log(func):
    def wrapper(*args, **kwargs):
        print("记录日志...")
        return func()              # 忘了把参数传下去！
    return wrapper


@log
def greet(name: str) -> str:
    return f"你好，{name}"


try:
    greet("小明")
except TypeError as e:
    print("报错：", e)
