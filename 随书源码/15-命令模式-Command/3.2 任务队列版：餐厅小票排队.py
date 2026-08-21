# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #3：3.2 任务队列版：餐厅小票排队
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from collections import deque


class Kitchen:
    """接收者：后厨"""

    def __init__(self):
        self.dishes = []

    def cook(self, dish: str) -> None:
        self.dishes.append(dish)
        print(f"后厨做好：{dish}（当前共 {len(self.dishes)} 道）")


class OrderCommand:
    """具体命令：一张点菜单"""

    def __init__(self, kitchen: Kitchen, dish: str):
        self.kitchen = kitchen
        self.dish = dish

    def execute(self) -> None:
        self.kitchen.cook(self.dish)


class Waiter:
    """调用者：服务员，负责记单、排队、退单、传菜"""

    def __init__(self, kitchen: Kitchen):
        self.kitchen = kitchen
        self.queue = deque()        # 未执行的点单，按顺序排队

    def take_order(self, dish: str) -> None:
        self.queue.append(OrderCommand(self.kitchen, dish))
        print(f"服务员记下点单：{dish}")

    def cancel_order(self, dish: str) -> None:
        """退单：从队列里移除还没做的菜"""
        before = len(self.queue)
        self.queue = deque(c for c in self.queue if c.dish != dish)
        removed = before - len(self.queue)
        print(f"退掉 {removed} 份还没做的「{dish}」")

    def send_to_kitchen(self) -> None:
        """把队列里所有单子一次性传给后厨"""
        print("--- 传单给后厨 ---")
        while self.queue:
            self.queue.popleft().execute()


kitchen = Kitchen()
waiter = Waiter(kitchen)
waiter.take_order("红烧肉")
waiter.take_order("清蒸鱼")
waiter.take_order("红烧肉")
waiter.cancel_order("红烧肉")        # 客人改主意了，退单
waiter.send_to_kitchen()
