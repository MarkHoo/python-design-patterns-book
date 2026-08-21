# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #12：误区 3：`__getattr__` 转发时的无限递归
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class RecursiveAdapter:
    """反面教材：__getattr__ 里访问自身不存在的属性 → 死循环"""

    def __getattr__(self, name):
        return self.anything   # self.anything 又不存在 → 又触发 __getattr__

try:
    RecursiveAdapter().foo
except RecursionError:
    print("触发 RecursionError：__getattr__ 无限递归")
