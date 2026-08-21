# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #3：3.2 订单状态通知：邮件 + 短信 + App
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import abc


class OrderNotifier(abc.ABC):
    """观察者：订单通知渠道"""

    @abc.abstractmethod
    def notify(self, order_id: str, status: str) -> None:
        pass


class EmailNotifier(OrderNotifier):
    def notify(self, order_id, status):
        print(f"  [邮件] 订单 {order_id} 状态：{status}")


class SmsNotifier(OrderNotifier):
    def notify(self, order_id, status):
        print(f"  [短信] 订单 {order_id} 状态：{status}")


class AppPushNotifier(OrderNotifier):
    def notify(self, order_id, status):
        print(f"  [App推送] 订单 {order_id} 状态：{status}")


class Order:
    """被观察者：订单状态变化时通知所有订阅渠道"""

    def __init__(self, order_id: str):
        self.order_id = order_id
        self.status = "待支付"
        self._channels = []

    def subscribe(self, channel: OrderNotifier) -> None:
        self._channels.append(channel)

    def unsubscribe(self, channel: OrderNotifier) -> None:
        self._channels.remove(channel)

    def update_status(self, new_status: str) -> None:
        self.status = new_status
        print(f"订单 {self.order_id} → {new_status}")
        for channel in self._channels:
            channel.notify(self.order_id, self.status)


order = Order("A001")
email, sms, app = EmailNotifier(), SmsNotifier(), AppPushNotifier()
order.subscribe(email)
order.subscribe(sms)

print("--- 只订了邮件和短信 ---")
order.update_status("已支付")

print("--- 用户又订了 App 推送 ---")
order.subscribe(app)
order.update_status("已发货")

print("--- 用户退订短信 ---")
order.unsubscribe(sms)
order.update_status("已签收")
