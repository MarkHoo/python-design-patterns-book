# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #4：3.3 简化版：用列表构建责任链
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Handler:
    """一个很薄的处理者：只有名字和上限"""

    def __init__(self, name, limit):
        self.name = name
        self.limit = limit

    def can_handle(self, amount):
        return amount <= self.limit

# 用列表构建责任链
handlers = [
    Handler("组长", 500),
    Handler("经理", 5000),
    Handler("总监", 50000),
]

def handle(amount):
    for h in handlers:                 # 从头到尾遍历，找第一个能处理的
        if h.can_handle(amount):
            return f"{h.name}批了 {amount} 元"
    return "无人能批，需要董事会"

for amount in (300, 3000, 30000, 300000):
    print(f"报销 {amount} 元 → {handle(amount)}")
