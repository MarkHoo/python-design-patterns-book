# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #8：4.3 `functools.lru_cache` 版："按参数区分"的单例
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import functools


class ConnectionPool:
    def __init__(self, url: str):
        self.url = url
        self._conns = []

    def add(self, conn: str) -> None:
        self._conns.append(conn)

    def __repr__(self):
        return f"<Pool {self.url} 连接数={len(self._conns)}>"


@functools.lru_cache(maxsize=None)
def get_pool(url: str) -> ConnectionPool:
    print(f"新建连接池：{url}")
    return ConnectionPool(url)


p1 = get_pool("mysql://主库")
p2 = get_pool("mysql://主库")
p3 = get_pool("mysql://读库")
p1.add("conn-1")
print("同 URL 共享同一池:", p1 is p2)
print("不同 URL 各自独立:", p1 is not p3)
print("p2 能看到 p1 添加的连接:", p2)
