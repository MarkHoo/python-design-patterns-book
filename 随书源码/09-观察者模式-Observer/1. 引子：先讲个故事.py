# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：订单类里写死通知渠道——加一个渠道就要改订单类
class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.status = "待支付"

    def update_status(self, new_status):
        self.status = new_status
        print(f"订单 {self.order_id} 状态变更为：{new_status}")
        # ↓ 写死的通知逻辑：改订单状态还得顺带管通知
        self._send_email()
        self._send_sms()

    def _send_email(self):
        print(f"  [邮件] 订单 {self.order_id} 状态更新：{self.status}")

    def _send_sms(self):
        print(f"  [短信] 订单 {self.order_id} 状态更新：{self.status}")


order = Order("A001")
order.update_status("已支付")
order.update_status("已发货")
