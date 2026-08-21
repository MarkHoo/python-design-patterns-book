# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #6：4.2 用 `weakref` 弱引用，避免"观察者泄漏在主题里"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import gc
import weakref


class Subject:
    """主题：用弱引用保存观察者，避免泄漏"""

    def __init__(self):
        self._observers = []

    def attach(self, observer) -> None:
        # 存的是弱引用，不增加对象的"存活负担"
        self._observers.append(weakref.ref(observer))

    def notify(self, message: str) -> None:
        alive = []
        for ref in self._observers:
            observer = ref()
            if observer is not None:
                observer.update(message)
                alive.append(ref)
            # observer 已被回收？弱引用取到 None，自动清掉
        self._observers = alive


class Widget:
    def __init__(self, name: str):
        self.name = name

    def update(self, message: str) -> None:
        print(f"  [{self.name}] 收到：{message}")


subject = Subject()
w1 = Widget("窗口A")
w2 = Widget("窗口B")
subject.attach(w1)
subject.attach(w2)

print("--- 两个观察者都在 ---")
subject.notify("刷新列表")

# w1 被销毁了，但没人记得调用 detach
del w1
gc.collect()

print("--- w1 已被回收，通知不再报错 ---")
subject.notify("再次刷新")
print("剩余观察者数量：", len(subject._observers))
