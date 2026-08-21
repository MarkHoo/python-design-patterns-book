# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #9：误区 1：回调抛异常导致通知中断
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, fn):
        self._observers.append(fn)

    def notify_bad(self, msg):     # 反面：一个观察者炸了，后面的全收不到
        for fn in self._observers:
            fn(msg)

    def notify_good(self, msg):    # 正确：每个通知都包一层 try/except
        for fn in self._observers:
            try:
                fn(msg)
            except Exception as e:
                print(f"  观察者 {fn.__name__} 出错，已隔离：{e}")


def observer_a(msg):
    print(f"  [A] 收到 {msg}")


def observer_b(msg):
    raise ValueError("B 的处理逻辑炸了")


def observer_c(msg):
    print(f"  [C] 收到 {msg}")


s = Subject()
s.attach(observer_a)
s.attach(observer_b)
s.attach(observer_c)

print("--- 反面：通知中断 ---")
try:
    s.notify_bad("事件1")
except ValueError as e:
    print("  异常冒泡上来，C 永远收不到：", e)

print("--- 正确：异常隔离 ---")
s.notify_good("事件2")
