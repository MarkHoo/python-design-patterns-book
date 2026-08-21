# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #14：练习 2：状态类版订单（状态对象里转移）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：每个状态类知道"下一个状态是谁"
class PendingState:
    def pay(self, order) -> None:
        print("待支付 → 已支付")
        order.state = PaidState()

    def cancel(self, order) -> None:
        print("待支付 → 已取消")
        order.state = CancelledState()


class PaidState:
    def ship(self, order) -> None:
        print("已支付 → 已发货")
        order.state = ShippedState()


class ShippedState:
    def complete(self, order) -> None:
        print("已发货 → 已完成")
        order.state = DoneState()


class DoneState:
    def pay(self, order) -> None:
        print("订单已完成，不能再支付")


class CancelledState:
    def pay(self, order) -> None:
        print("订单已取消，无法支付")


class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.state = PendingState()

    def pay(self) -> None:
        self.state.pay(self)

    def ship(self) -> None:
        self.state.ship(self)

    def complete(self) -> None:
        self.state.complete(self)


order = Order("A2002")
order.pay()
order.ship()
order.complete()
order.pay()
