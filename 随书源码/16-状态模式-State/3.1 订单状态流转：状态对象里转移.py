# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #2：3.1 订单状态流转：状态对象里转移
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class PendingState:
    """待支付：只能支付或取消"""

    def pay(self, order) -> None:
        print("待支付 → 已支付")
        order.state = PaidState()

    def cancel(self, order) -> None:
        print("待支付 → 已取消")
        order.state = CancelledState()


class PaidState:
    """已支付：只能发货"""

    def ship(self, order) -> None:
        print("已支付 → 已发货")
        order.state = ShippedState()


class ShippedState:
    """已发货：只能确认完成"""

    def complete(self, order) -> None:
        print("已发货 → 已完成")
        order.state = DoneState()


class DoneState:
    """已完成：终态，什么都不许做"""

    def pay(self, order) -> None:
        print("订单已完成，不能再支付")

    def ship(self, order) -> None:
        print("订单已完成，不能发货")

    def complete(self, order) -> None:
        print("订单已经完成了")


class CancelledState:
    """已取消：终态"""

    def pay(self, order) -> None:
        print("订单已取消，无法支付")


class Order:
    """上下文：只管转发请求 + 持有当前状态"""

    def __init__(self, order_id: str):
        self.order_id = order_id
        self.state = PendingState()

    def pay(self) -> None:
        self.state.pay(self)

    def ship(self) -> None:
        self.state.ship(self)

    def complete(self) -> None:
        self.state.complete(self)


order = Order("A1001")
order.pay()
order.ship()
order.complete()
order.pay()          # 已完成订单想再支付？状态类直接拒绝
