# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有访问者的世界——isinstance 链到处复制粘贴
class Number:
    def __init__(self, value: int):
        self.value = value

class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

def evaluate(node) -> int:
    """求值：每加一种节点，这里就要加一个 elif"""
    if isinstance(node, Number):
        return node.value
    elif isinstance(node, Add):
        return evaluate(node.left) + evaluate(node.right)

def count_nodes(node) -> int:
    """统计节点数：又是一条一模一样的 isinstance 链！"""
    if isinstance(node, Number):
        return 1
    elif isinstance(node, Add):
        return 1 + count_nodes(node.left) + count_nodes(node.right)

expr = Add(Number(1), Add(Number(2), Number(3)))
print("求值结果：", evaluate(expr))
print("节点总数：", count_nodes(expr))
