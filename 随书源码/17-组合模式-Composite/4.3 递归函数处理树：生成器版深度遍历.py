# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #7：4.3 递归函数处理树：生成器版深度遍历
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class File:
    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return ()


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)


def walk(node, depth: int = 0):
    """递归遍历：生成器版，产出 (节点, 深度)"""
    yield node, depth
    for child in node.children:
        yield from walk(child, depth + 1)


root = Folder("root")
src = Folder("src")
src.add(File("main.py"))
src.add(File("utils.py"))
root.add(src)
root.add(File("README.md"))

for node, depth in walk(root):
    print("  " * depth + node.name)
