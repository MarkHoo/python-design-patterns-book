# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #2：3.1 经典版：文件系统
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class FileNode:
    """组件接口：叶子（文件）和容器（文件夹）的统一接口"""

    @property
    def children(self):
        """默认没有子节点——叶子返回空，容器返回子节点列表"""
        return ()

    def open(self) -> str:
        raise NotImplementedError

    def add(self, child) -> None:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError


class File(FileNode):
    """叶子：文件"""

    def __init__(self, name: str, size: int):
        self.name = name
        self._size = size

    def open(self) -> str:
        return f"打开文件 {self.name}（{self._size} KB）"

    def add(self, child) -> None:
        raise ValueError("文件不能包含子节点")

    def size(self) -> int:
        return self._size


class Folder(FileNode):
    """容器：文件夹"""

    def __init__(self, name: str):
        self.name = name
        self._children = []

    @property
    def children(self):
        return self._children

    def open(self) -> str:
        return f"打开文件夹 {self.name}（{len(self._children)} 个条目）"

    def add(self, child) -> None:
        self._children.append(child)

    def size(self) -> int:
        return sum(child.size() for child in self._children)   # 递归求总大小


def print_tree(node: FileNode, indent: str = "") -> None:
    """客户端只认 FileNode：叶子与容器一视同仁，零类型判断"""
    print(indent + node.open())
    for child in node.children:
        print_tree(child, indent + "  ")


root = Folder("工作")
docs = Folder("文档")
docs.add(File("需求.md", 12))
docs.add(File("设计.md", 45))
root.add(docs)
root.add(File("README.txt", 3))

print_tree(root)
print("整个工作目录总大小:", root.size(), "KB")
