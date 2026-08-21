# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》09-观察者模式-Observer
# 代码块 #8：标准库：`asyncio.Future.add_done_callback`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import asyncio


def on_done(task) -> None:
    """观察者回调：任务完成时被调用"""
    print("回调收到任务结果：", task.result())


async def download() -> str:
    await asyncio.sleep(0.05)
    return "下载完成，共 1.2MB"


async def main() -> None:
    task = asyncio.create_task(download())   # 被观察者：任务
    task.add_done_callback(on_done)          # 注册观察者：完成回调
    await task                               # 等任务完成
    print("主流程继续：任务已结束")


asyncio.run(main())
