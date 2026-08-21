# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #5：3.3 带参数的装饰器：三层函数
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def repeat(times: int):
    """装饰器工厂：让函数重复执行 times 次"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper

    return decorator


@repeat(3)
def roll_dice() -> str:
    return "🎲 掷出 6 点"


print(roll_dice())
