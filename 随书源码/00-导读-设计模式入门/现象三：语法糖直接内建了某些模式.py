# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》00-导读-设计模式入门
# 代码块 #11：现象三：语法糖直接内建了某些模式
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import functools

@functools.lru_cache(maxsize=None)
def fib(n: int) -> int:
    """带缓存的斐波那契——装饰器模式 + 备忘录思想，一行搞定"""
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(fib(50))
print(f"缓存命中信息：{fib.cache_info()}")
