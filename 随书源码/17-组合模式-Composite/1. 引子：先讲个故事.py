# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有组合的世界——文件和文件夹分开处理，调用方要判类型
class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def open(self):
        print(f"打开文件：{self.name}（{self.size} KB）")


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def open(self):
        print(f"打开文件夹：{self.name}（{len(self.children)} 个条目）")


def show(node) -> None:
    # 调用方被迫区分类型——加新类型（快捷方式、压缩包）就要改这里
    if isinstance(node, File):
        node.open()
    elif isinstance(node, Folder):
        print(f"进入文件夹 {node.name}")
        for child in node.children:
            show(child)


root = Folder("工作")
docs = Folder("文档")
docs.add(File("需求.md", 12))
docs.add(File("设计.md", 45))
root.add(docs)
root.add(File("README.txt", 3))
show(root)
