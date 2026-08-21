# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #11：误区 3：忘记线程安全
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import threading

class SafeFactory:
    """线程安全的享元工厂：加锁 + 双重检查"""

    def __init__(self):
        self._pool = {}
        self._lock = threading.Lock()

    def get(self, key):
        if key not in self._pool:          # 快速路径：不加锁
            with self._lock:               # 慢路径：加锁
                if key not in self._pool:  # 双重检查
                    self._pool[key] = (key, len(self._pool))
        return self._pool[key]

factory = SafeFactory()
results = []

def worker():
    results.append(factory.get("共享资源"))

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("10 个线程拿到的都是同一个对象:", len({id(r) for r in results}) == 1)
