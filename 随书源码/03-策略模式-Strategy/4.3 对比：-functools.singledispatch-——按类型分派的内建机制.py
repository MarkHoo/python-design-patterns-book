# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #7：4.3 对比：`functools.singledispatch`——按类型分派的内建机制
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from functools import singledispatch


@singledispatch
def format_data(data):
    return f"未知类型：{type(data).__name__}"


@format_data.register
def _(data: str):
    return f"字符串：{data}"


@format_data.register
def _(data: int):
    return f"整数：{data}"


@format_data.register
def _(data: list):
    return f"列表（{len(data)} 项）：{data}"


print(format_data("你好"))
print(format_data(42))
print(format_data([1, 2, 3]))
print(format_data(3.14))
