# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #10：误区 2：忘记注销观察者，内存泄漏
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import gc


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, o):
        self._observers.append(o)


class BigWidget:
    def __init__(self, name):
        self.name = name

    def update(self, msg):
        pass


s = Subject()
w = BigWidget("大窗口")
s.attach(w)
print("删除前，主题持有观察者数量：", len(s._observers))

del w            # 窗口关了，但忘了 detach
gc.collect()

count = sum(1 for obj in gc.get_objects() if type(obj).__name__ == "BigWidget")
print("删除后，BigWidget 实例仍存活：", count, "（被主题强引用，无法回收——泄漏！）")
