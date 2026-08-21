# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #11：练习 1：修复线程安全隐患
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import threading


class SafeConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# 答案：加锁 + 双重检查
class SafeConfig:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance


instances = []
threads = [threading.Thread(target=lambda: instances.append(SafeConfig())) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print("10 个线程拿到同一实例:", len({id(i) for i in instances}) == 1)
