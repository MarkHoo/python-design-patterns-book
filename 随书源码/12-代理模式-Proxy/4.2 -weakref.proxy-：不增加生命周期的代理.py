# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #6：4.2 `weakref.proxy`：不增加生命周期的代理
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import weakref

class BigData:
    def __init__(self, size):
        self.size = size
        print(f"加载了 {size} 条数据")

    def summary(self):
        return f"共 {self.size} 条数据"

data = BigData(10000)
ref = weakref.proxy(data)      # 弱引用代理：不阻止对象被回收
print("通过代理访问：", ref.summary())

del data                        # 真实对象被销毁
try:
    print(ref.summary())        # 代理指向的对象没了 → 报错
except ReferenceError:
    print("代理报错：原对象已被回收（ReferenceError）")
