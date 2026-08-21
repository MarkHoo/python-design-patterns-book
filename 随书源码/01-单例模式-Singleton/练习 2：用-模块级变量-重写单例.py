# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #12：练习 2：用"模块级变量"重写单例
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：模块级单例（真实项目里存成 cache.py，然后 `from cache import cache`）
class Cache:
    def __init__(self):
        self._store = {}

    def put(self, key, value):
        self._store[key] = value

    def get(self, key):
        return self._store.get(key)


cache = Cache()  # 模块顶层只执行一次 → 天然单例

# 模拟两个调用方各自 import
caller_a = cache
caller_b = cache
caller_a.put("user:1", "小明")
print("调用方 B 能看到 A 写入的数据:", caller_b.get("user:1"))
print("两边是同一个对象:", caller_a is caller_b)
