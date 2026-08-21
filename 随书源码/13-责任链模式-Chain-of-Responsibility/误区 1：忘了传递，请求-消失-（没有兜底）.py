# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #8：误区 1：忘了传递，请求"消失"（没有兜底）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Handler:
    def __init__(self):
        self._next = None

    def set_next(self, h):
        self._next = h
        return h

    def handle(self, amount):
        if self._next:
            return self._next.handle(amount)
        return None   # 兜底：无人处理返回 None

class Leader(Handler):
    def handle(self, amount):
        if amount <= 500:
            return "组长批了"
        return super().handle(amount)

class Manager(Handler):
    def handle(self, amount):
        if amount <= 5000:
            return "经理批了"
        return super().handle(amount)

# 反面教材：忘了加兜底节点，超大金额直接"消失"
chain = Leader()
chain.set_next(Manager())

result = chain.handle(99999)
if result is None:
    print("危险：99999 元的报销没有任何人处理，静默消失了！")
else:
    print(result)
