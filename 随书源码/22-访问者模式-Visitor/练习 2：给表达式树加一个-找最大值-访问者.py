# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #12：练习 2：给表达式树加一个"找最大值"访问者
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：新增访问者，元素类一行不动
class Number:
    def __init__(self, value: int):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_number(self)

class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_add(self)

class MaxFinder:
    def visit_number(self, node: Number) -> int:
        return node.value

    def visit_add(self, node: Add) -> int:
        return max(node.left.accept(self), node.right.accept(self))

expr = Add(Number(7), Add(Number(3), Number(9)))
print("最大数字：", expr.accept(MaxFinder()))
