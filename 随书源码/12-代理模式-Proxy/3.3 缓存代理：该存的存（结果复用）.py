# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #4：3.3 缓存代理：该存的存（结果复用）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import time

class SlowCalculator:
    """真实对象：计算很慢"""

    def calculate(self, n):
        time.sleep(0.2)        # 模拟 0.2 秒的昂贵计算
        return n * n

class CacheProxy:
    """缓存代理：同样的请求直接返回上次结果"""

    def __init__(self, target):
        self._target = target
        self._cache = {}

    def calculate(self, n):
        if n not in self._cache:
            self._cache[n] = self._target.calculate(n)
            print(f"（首次计算 {n}²，慢）")
        else:
            print(f"（命中缓存 {n}²，秒回）")
        return self._cache[n]

proxy = CacheProxy(SlowCalculator())
print(proxy.calculate(7))
print(proxy.calculate(7))
print(proxy.calculate(8))
print(proxy.calculate(8))
