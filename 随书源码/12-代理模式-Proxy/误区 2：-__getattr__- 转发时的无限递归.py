# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #9：误区 2：`__getattr__` 转发时的无限递归
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class RecursiveProxy:
    """反面教材：转发时访问了自己不存在的属性 → 无限递归"""

    def __getattr__(self, name):
        return self.missing_attribute   # self.missing_attribute 又不存在 → 又触发 __getattr__

try:
    RecursiveProxy().foo
except RecursionError:
    print("触发 RecursionError：__getattr__ 无限递归")
