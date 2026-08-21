# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》15-命令模式-Command
# 代码块 #8：标准库：`concurrent.futures` 的"任务对象"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import concurrent.futures


def upload(url: str, data: str) -> str:
    """模拟一个耗时的上传任务"""
    return f"已上传 {data} 到 {url}"


# 把"函数 + 参数"打包成任务对象提交——每个任务就是一个命令
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures = [
        pool.submit(upload, "http://cdn.example.com/a", "图片A"),
        pool.submit(upload, "http://cdn.example.com/b", "图片B"),
    ]
    for f in futures:             # 按提交顺序取结果
        print(f.result())
