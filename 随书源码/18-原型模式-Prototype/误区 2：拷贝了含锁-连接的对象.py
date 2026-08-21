# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #10：误区 2：拷贝了含锁/连接的对象
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy
import threading

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    def increment(self):
        with self.lock:
            self.value += 1
            return self.value


c1 = Counter()
try:
    c2 = copy.deepcopy(c1)   # 想复制一个计数器？
except TypeError as e:
    print("深拷贝失败：", e)

print("原因：锁是资源，不允许被复制")
