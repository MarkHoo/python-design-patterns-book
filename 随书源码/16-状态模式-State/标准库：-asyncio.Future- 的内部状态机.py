# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》16-状态模式-State
# 代码块 #8：标准库：`asyncio.Future` 的内部状态机
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import asyncio


async def demo() -> None:
    future = asyncio.Future()
    print("创建后的状态:", future._state)          # PENDING
    future.set_result(42)
    print("set_result 后的状态:", future._state)  # FINISHED
    print("拿到结果:", future.result())

    cancelled = asyncio.Future()
    cancelled.cancel()
    print("取消后的状态:", cancelled._state)       # CANCELLED


asyncio.run(demo())
