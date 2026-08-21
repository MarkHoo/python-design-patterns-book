# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #8：标准库：`asyncio` 的事件循环策略
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import asyncio


class MyEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    """自定义策略：工厂方法 new_event_loop 由子类决定"""

    def new_event_loop(self):
        loop = super().new_event_loop()
        print("（自定义策略）事件循环已创建")
        return loop


policy = MyEventLoopPolicy()
loop = policy.new_event_loop()      # 工厂方法：造一个事件循环
print("是个合格的事件循环：", isinstance(loop, asyncio.AbstractEventLoop))
loop.close()
