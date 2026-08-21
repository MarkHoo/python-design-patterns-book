# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #11：误区 3：依赖通知顺序
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面：观察者 A 假设自己一定在 B 之前被通知
class Order:
    def __init__(self):
        self._observers = []

    def attach(self, fn, name):
        self._observers.append((name, fn))

    def notify(self):
        for name, fn in self._observers:
            fn(name)


def first(name):
    print(f"{name} 先执行：扣库存")


def second(name):
    print(f"{name} 后执行：发货")


o = Order()
o.attach(first, "A")
o.attach(second, "B")
o.notify()

print("--- 换个注册顺序，结果就变了 ---")
o2 = Order()
o2.attach(second, "B")
o2.attach(first, "A")
o2.notify()
