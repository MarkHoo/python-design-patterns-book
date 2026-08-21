# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #14：练习 3：用 `weakref` 修复"忘了注销"的泄漏
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：弱引用保存观察者，对象回收后自动失效
import gc
import weakref


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, o):
        self._observers.append(weakref.ref(o))

    def notify(self, msg):
        alive = []
        for ref in self._observers:
            o = ref()
            if o is not None:
                o.update(msg)
                alive.append(ref)
        self._observers = alive


class Listener:
    def __init__(self, name):
        self.name = name

    def update(self, msg):
        print(f"  [{self.name}] {msg}")


s = Subject()
a = Listener("甲")
b = Listener("乙")
s.attach(a)
s.attach(b)

del a          # 甲被销毁，但忘了注销
gc.collect()

s.notify("你好")
print("剩余观察者：", len(s._observers))
