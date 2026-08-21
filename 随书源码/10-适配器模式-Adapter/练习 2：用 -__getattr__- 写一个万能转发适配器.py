# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》10-适配器模式-Adapter
# 代码块 #15：练习 2：用 `__getattr__` 写一个万能转发适配器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：__getattr__ 自动转发
class LegacyService:
    def fetch_orders(self):
        return ["订单1", "订单2"]

    def fetch_users(self):
        return ["用户1", "用户2"]

class ServiceAdapter:
    """万能转发适配器"""

    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        return getattr(self._target, name)

adapter = ServiceAdapter(LegacyService())
print(adapter.fetch_orders())
print(adapter.fetch_users())
