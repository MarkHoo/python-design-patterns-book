# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #5：4.1 鸭子类型统一接口：不需要抽象基类
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class File:
    """叶子"""

    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return ()          # 叶子没有孩子

    def size(self) -> int:
        return 10          # 假设每个文件 10 KB


class Folder:
    """容器"""

    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def size(self) -> int:
        return sum(child.size() for child in self.children)


def total_size(node) -> int:
    """不需要类型判断，也不需要抽象基类——长得像节点就行"""
    return node.size()


root = Folder("项目")
root.add(File("a.py"))
root.add(File("b.py"))
print("总大小:", total_size(root), "KB")
print("单个文件大小:", total_size(File("c.py")), "KB")
