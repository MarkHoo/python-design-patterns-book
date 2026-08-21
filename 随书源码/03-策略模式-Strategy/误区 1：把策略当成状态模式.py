# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #9：误区 1：把策略当成状态模式
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 误区 1：策略 ≠ 状态。下面演示状态模式的"自动切换"：
class PaidState:
    def next(self, order):
        order.state = ShippedState()
        return "已支付 → 已发货"


class ShippedState:
    def next(self, order):
        order.state = DoneState()
        return "已发货 → 已完成"


class DoneState:
    def next(self, order):
        return "订单已完成，不能继续流转"


class Order:
    def __init__(self):
        self.state = PaidState()

    def advance(self):
        return self.state.next(self)


order = Order()
for _ in range(3):
    print(order.advance())   # 状态自己变，不用客户端操心
