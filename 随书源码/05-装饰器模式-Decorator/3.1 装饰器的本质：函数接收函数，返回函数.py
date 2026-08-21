# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #3：3.1 装饰器的本质：函数接收函数，返回函数
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def add_logging(func):
    """包装函数：调用前打日志"""
    def wrapper(*args, **kwargs):
        print(f"[日志] 调用 {func.__name__}，参数 {args}")
        return func(*args, **kwargs)
    return wrapper


def add(a: int, b: int) -> int:
    return a + b


add_with_log = add_logging(add)      # 手动包装：add 本体没动
print("结果：", add_with_log(1, 2))
print("原函数还是原函数：", add(1, 2))
