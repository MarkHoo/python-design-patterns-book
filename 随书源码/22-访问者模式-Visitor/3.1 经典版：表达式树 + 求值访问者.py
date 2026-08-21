# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #2：3.1 经典版：表达式树 + 求值访问者
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 经典访问者：表达式树（元素）+ 求值（访问者）
class Number:
    """数字节点：只有值，没有子节点"""

    def __init__(self, value: int):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_number(self)

class Add:
    """加法节点：左右各一个子表达式"""

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_add(self)

class Evaluator:
    """访问者：求值器"""

    def visit_number(self, node: Number) -> int:
        return node.value

    def visit_add(self, node: Add) -> int:
        return node.left.accept(self) + node.right.accept(self)

expr = Add(Number(1), Add(Number(2), Number(3)))
print("求值结果：", expr.accept(Evaluator()))
