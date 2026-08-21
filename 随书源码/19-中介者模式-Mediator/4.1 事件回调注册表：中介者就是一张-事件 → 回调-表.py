# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》19-中介者模式-Mediator
# 代码块 #5：4.1 事件回调注册表：中介者就是一张"事件 → 回调"表
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class EventMediator:
    """事件注册表式中介者：内部就是一张 {事件名: [回调函数]} 的表"""
    def __init__(self):
        self._handlers = {}
    def on(self, event, handler):
        self._handlers.setdefault(event, []).append(handler)
    def emit(self, event, *args):
        for handler in self._handlers.get(event, []):
            handler(*args)


def refresh_list(data):
    print(f"列表框刷新：{data}")


def update_status(data):
    print(f"状态栏更新：收到 {len(data)} 条数据")


def notify_admin(data):
    print(f"管理员收到通知：{data}")


mediator = EventMediator()
for h in (refresh_list, update_status, notify_admin):
    mediator.on("data_loaded", h)

mediator.emit("data_loaded", ["苹果", "香蕉", "橙子"])
print("---")
mediator.emit("data_loaded", ["只有一条"])
