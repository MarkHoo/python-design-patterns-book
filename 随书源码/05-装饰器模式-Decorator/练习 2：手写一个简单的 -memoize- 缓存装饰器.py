# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #16：练习 2：手写一个简单的 `memoize` 缓存装饰器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def memoize(func):
    cache = {}

    def wrapper(n: int) -> int:
        if n not in cache:
            cache[n] = func(n)
            print(f"计算 fib({n})")
        return cache[n]
    return wrapper


@memoize
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print("fib(6) =", fib(6))
