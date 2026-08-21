# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #11：练习 1：写一个客服工单转接链
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：经典责任链
class SupportHandler:
    def __init__(self, name, max_difficulty):
        self.name = name
        self.max_difficulty = max_difficulty
        self._next = None

    def set_next(self, h):
        self._next = h
        return h

    def handle(self, ticket):
        if ticket <= self.max_difficulty:
            return f"{self.name}解决了难度 {ticket} 的工单"
        if self._next:
            return self._next.handle(ticket)
        return "工单升级到最高层处理"

chain = SupportHandler("一线客服", 2)
chain.set_next(SupportHandler("组长", 4)).set_next(SupportHandler("经理", 6))

for difficulty in (1, 3, 5, 9):
    print(chain.handle(difficulty))
