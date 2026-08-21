# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #9：误区 1：改了结构，忘了同步访问者
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 误区：新增节点类型，老访问者没有对应方法 → 运行期才炸
class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Evaluator:
    def visit_number(self, node) -> int:
        return node.value

    def visit_add(self, node) -> int:
        return node.left.accept(self) + node.right.accept(self)

expr = Multiply(Multiply(2, 3), 4)
try:
    print(expr.accept(Evaluator()))
except AttributeError as e:
    print("运行期才炸：", e)
