# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #11：误区 3：在树里引入循环引用
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Node:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)


root = Node("root")
child = Node("child")
root.add(child)
child.add(root)          # 树变成了环！遍历会永远转圈


def walk(node, depth: int = 0) -> None:
    print("  " * depth + node.name)
    if depth >= 3:                       # 人为设个深度上限，模拟"发现不对劲"
        print("...还在循环（正常遍历早该结束了）")
        return
    for c in node.children:
        walk(c, depth + 1)


walk(root)
