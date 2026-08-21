# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #4：3.3 事件系统变体：按事件名订阅
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class EventBus:
    """迷你事件总线：按事件名订阅，一对多广播"""

    def __init__(self):
        self._handlers = {}

    def on(self, event: str, handler) -> None:
        """订阅：给某类事件注册处理器"""
        self._handlers.setdefault(event, []).append(handler)

    def off(self, event: str, handler) -> None:
        self._handlers[event].remove(handler)

    def emit(self, event: str, payload) -> None:
        """发布：触发某类事件的所有处理器"""
        print(f"触发事件：{event}")
        for handler in self._handlers.get(event, []):
            handler(payload)


def log_order(payload):
    print(f"  [日志] 记录订单 {payload}")


def send_coupon(payload):
    print(f"  [营销] 给订单 {payload} 发优惠券")


bus = EventBus()
bus.on("order.created", log_order)
bus.on("order.created", send_coupon)
bus.on("order.paid", log_order)

bus.emit("order.created", "A001")
bus.emit("order.paid", "A001")
