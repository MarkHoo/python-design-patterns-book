# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #7：4.3 `@dataclass` 事件对象
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from dataclasses import dataclass


@dataclass
class OrderEvent:
    """事件对象：携带完整上下文，比裸参数更清晰"""
    order_id: str
    status: str
    amount: float = 0.0
    note: str = ""


class OrderTracker:
    """被观察者：发布 OrderEvent 事件对象"""

    def __init__(self):
        self._handlers = []

    def on_change(self, handler) -> None:
        self._handlers.append(handler)

    def change(self, event: OrderEvent) -> None:
        print(f"状态变更：{event.order_id} → {event.status}")
        for handler in self._handlers:
            handler(event)


def audit_log(event: OrderEvent) -> None:
    print(f"  [审计] {event.order_id} {event.status} 金额={event.amount} 备注={event.note}")


def notify_user(event: OrderEvent) -> None:
    if event.status == "已退款":
        print(f"  [通知] 您的订单 {event.order_id} 已退款 {event.amount} 元")


tracker = OrderTracker()
tracker.on_change(audit_log)
tracker.on_change(notify_user)

tracker.change(OrderEvent(order_id="A001", status="已支付", amount=199.0))
tracker.change(OrderEvent(order_id="A001", status="已退款", amount=199.0, note="七天无理由"))
