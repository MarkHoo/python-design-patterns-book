# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #10：误区 3：懒加载代理的线程安全问题
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import threading
import time

class Heavy:
    def __init__(self):
        time.sleep(0.05)
        self.ready = True

class LazyProxy:
    """线程安全懒加载代理：加锁 + 双重检查"""

    def __init__(self, factory):
        self._factory = factory
        self._real = None
        self._lock = threading.Lock()

    def get(self):
        if self._real is None:            # 第一次检查：不加锁，快路径
            with self._lock:
                if self._real is None:    # 第二次检查：防止重复创建
                    self._real = self._factory()
        return self._real

proxy = LazyProxy(lambda: Heavy())
results = []
lock = threading.Lock()

def worker():
    obj = proxy.get()
    with lock:
        results.append(obj)

threads = [threading.Thread(target=worker) for _ in range(8)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("8 个线程拿到的都是同一个实例：", len({id(r) for r in results}) == 1)
