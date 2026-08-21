# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #6：4.2 dataclass 状态元数据 + 转移表
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from dataclasses import dataclass
from enum import Enum


class OrderStatus(Enum):
    PENDING = "待支付"
    PAID = "已支付"
    SHIPPED = "已发货"
    DONE = "已完成"
    CANCELLED = "已取消"


@dataclass(frozen=True)
class StatusInfo:
    """状态元数据：这个状态下允许哪些动作"""
    label: str
    allowed_actions: tuple


STATUS_INFO = {
    OrderStatus.PENDING: StatusInfo("待支付", ("pay", "cancel")),
    OrderStatus.PAID: StatusInfo("已支付", ("ship",)),
    OrderStatus.SHIPPED: StatusInfo("已发货", ("complete",)),
    OrderStatus.DONE: StatusInfo("已完成", ()),
    OrderStatus.CANCELLED: StatusInfo("已取消", ()),
}

# 状态转移表：(状态, 动作) → 下一状态
TRANSITIONS = {
    (OrderStatus.PENDING, "pay"): OrderStatus.PAID,
    (OrderStatus.PENDING, "cancel"): OrderStatus.CANCELLED,
    (OrderStatus.PAID, "ship"): OrderStatus.SHIPPED,
    (OrderStatus.SHIPPED, "complete"): OrderStatus.DONE,
}


class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.status = OrderStatus.PENDING

    def do(self, action: str) -> None:
        info = STATUS_INFO[self.status]
        if action not in info.allowed_actions:
            raise ValueError(f"订单 {self.order_id} 当前是「{info.label}」，不能执行 {action}")
        self.status = TRANSITIONS[(self.status, action)]
        print(f"订单 {self.order_id} 执行 {action} → {STATUS_INFO[self.status].label}")


order = Order("A2001")
order.do("pay")
order.do("ship")
order.do("complete")
try:
    order.do("pay")        # 已完成订单不能再支付
except ValueError as e:
    print("非法操作被拦截:", e)
