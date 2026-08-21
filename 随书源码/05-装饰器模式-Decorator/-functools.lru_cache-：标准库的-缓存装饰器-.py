# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #11：`functools.lru_cache`：标准库的"缓存装饰器"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import functools


@functools.lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print("fib(40) =", fib(40))
print("缓存统计：", fib.cache_info())
