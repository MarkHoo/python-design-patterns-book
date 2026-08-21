# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #2：3.1 经典版：手拉手构建审批链（遇能处理者即停）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Handler:
    """责任链节点：处理不了就传给下一个"""

    def __init__(self):
        self._next = None

    def set_next(self, handler):
        """把下一个处理者接在自己后面（返回它以便继续链式）"""
        self._next = handler
        return handler

    def handle(self, amount):
        if self._next:
            return self._next.handle(amount)
        return "无人能批，需要董事会"

class TeamLeader(Handler):
    """组长：500 以内自己批"""

    def handle(self, amount):
        if amount <= 500:
            return f"组长批了 {amount} 元"
        return super().handle(amount)

class Manager(Handler):
    """经理：5000 以内自己批"""

    def handle(self, amount):
        if amount <= 5000:
            return f"经理批了 {amount} 元"
        return super().handle(amount)

class Director(Handler):
    """总监：50000 以内自己批"""

    def handle(self, amount):
        if amount <= 50000:
            return f"总监批了 {amount} 元"
        return super().handle(amount)

# 手拉手构建责任链：组长 → 经理 → 总监
leader = TeamLeader()
leader.set_next(Manager()).set_next(Director())

for amount in (300, 3000, 30000, 300000):
    print(f"报销 {amount} 元 → {leader.handle(amount)}")
