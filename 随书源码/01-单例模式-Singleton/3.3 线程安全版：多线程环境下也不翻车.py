# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #4：3.3 线程安全版：多线程环境下也不翻车
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import threading


class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:        # 第一次检查：不加锁，快路径
            with cls._lock:              # 拿到锁
                if cls._instance is None:  # 第二次检查：防止重复创建
                    cls._instance = super().__new__(cls)
        return cls._instance


def worker(results):
    results.append(ThreadSafeSingleton())


results = []
threads = [threading.Thread(target=worker, args=(results,)) for _ in range(8)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("8 个线程拿到的都是同一个实例:", len({id(r) for r in results}) == 1)
