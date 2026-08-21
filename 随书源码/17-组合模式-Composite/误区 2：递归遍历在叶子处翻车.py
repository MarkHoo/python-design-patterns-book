# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #10：误区 2：递归遍历在叶子处翻车
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：遍历假设所有节点都有 children，叶子没有就炸
class File:
    def __init__(self, name: str):
        self.name = name


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.children = []


def walk(node, depth: int = 0) -> None:
    print("  " * depth + node.name)
    for child in node.children:          # File 没有 children → 炸
        walk(child, depth + 1)


root = Folder("root")
root.children.append(File("a.txt"))
try:
    walk(root)
except AttributeError as e:
    print("遍历在叶子处炸了:", e)
