# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #5：4.1 `__getattr__` 万能转发代理
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class GenericProxy:
    """通用代理：只负责转发，具体对象随便换"""

    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        # 代理自己没有的属性，全部转发给目标对象
        return getattr(self._target, name)

class Logger:
    def __init__(self, name):
        self.name = name

    def info(self, msg):
        print(f"[INFO] {self.name}: {msg}")

proxy = GenericProxy(Logger("订单服务"))
proxy.info("收到新订单")     # 代理没有 info → 转发给 Logger
print("代理能拿到属性：", proxy.name)
