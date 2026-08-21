# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》01-单例模式-Singleton
# 代码块 #13：练习 3：用 `lru_cache` 实现"每个参数一个实例"的注册表
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：functools.lru_cache 天然就是"按参数去重"的注册表
import functools


class Driver:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.sessions = 0

    def connect(self):
        self.sessions += 1
        return f"{self.db_name} 第 {self.sessions} 个会话"


@functools.lru_cache(maxsize=None)
def get_driver(db_name: str) -> Driver:
    print(f"创建驱动：{db_name}")
    return Driver(db_name)


d1 = get_driver("订单库")
d2 = get_driver("订单库")
d3 = get_driver("用户库")
d1.connect()
print("同库共享驱动:", d1 is d2)
print("不同库独立:", d1 is not d3)
print("d2.connect():", d2.connect(), "（会话数共享，证明是同一个）")
