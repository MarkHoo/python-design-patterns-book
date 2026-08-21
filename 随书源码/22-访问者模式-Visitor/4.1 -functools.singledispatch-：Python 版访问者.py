# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #5：4.1 `functools.singledispatch`：Python 版访问者
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# singledispatch：按参数类型分派到不同函数——天然就是"访问者"
from functools import singledispatch

class Number:
    def __init__(self, value: int):
        self.value = value

class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

@singledispatch
def evaluate(node):
    raise TypeError(f"不知道如何求值：{type(node).__name__}")

@evaluate.register
def _(node: Number) -> int:
    return node.value

@evaluate.register
def _(node: Add) -> int:
    return evaluate(node.left) + evaluate(node.right)

expr = Add(Number(1), Add(Number(2), Number(3)))
print("求值结果：", evaluate(expr))
