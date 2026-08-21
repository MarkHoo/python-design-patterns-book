# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #8：5.2 `functools.singledispatch`：标准库里的"操作分派"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# singledispatch 的真实用例：给不同类型的对象做统一处理
from functools import singledispatch

@singledispatch
def describe(obj):
    return f"未知类型：{type(obj).__name__}"

@describe.register
def _(obj: int) -> str:
    return f"整数 {obj}，绝对值 {abs(obj)}"

@describe.register
def _(obj: str) -> str:
    return f"字符串 {obj!r}，长度 {len(obj)}"

@describe.register
def _(obj: list) -> str:
    return f"列表，共 {len(obj)} 个元素"

print(describe(42))
print(describe("访问者"))
print(describe([1, 2, 3]))
print(describe(1.5))
