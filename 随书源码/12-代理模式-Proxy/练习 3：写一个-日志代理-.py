# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》12-代理模式-Proxy
# 代码块 #13：练习 3：写一个"日志代理"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：__getattr__ 转发 + 调用前打日志
class LogProxy:
    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        attr = getattr(self._target, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                print(f"[日志] 调用 {name}，参数 {args}")
                return attr(*args, **kwargs)
            return wrapper
        return attr

class OrderService:
    def create(self, order_id):
        return f"订单 {order_id} 已创建"

    def cancel(self, order_id):
        return f"订单 {order_id} 已取消"

proxy = LogProxy(OrderService())
print(proxy.create(1001))
print(proxy.cancel(1001))
