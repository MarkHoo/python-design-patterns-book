# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #3：3.2 文件目录统计版（带状态的访问者）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 访问者版目录统计：文件/文件夹共享 accept，访问者各自统计
class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def accept(self, visitor):
        return visitor.visit_file(self)

class Directory:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> "Directory":
        self.children.append(child)
        return self

    def accept(self, visitor):
        return visitor.visit_directory(self)

class SizeCounter:
    def visit_file(self, node: File) -> int:
        return node.size

    def visit_directory(self, node: Directory) -> int:
        return sum(child.accept(self) for child in node.children)

class FileLister:
    """带状态的访问者：收集文件路径"""

    def __init__(self):
        self.paths = []
        self._prefix = ""

    def visit_file(self, node: File) -> None:
        self.paths.append(self._prefix + node.name)

    def visit_directory(self, node: Directory) -> None:
        old = self._prefix
        self._prefix = old + node.name + "/"
        for child in node.children:
            child.accept(self)
        self._prefix = old

root = (Directory("项目")
        .add(File("README.md", 2))
        .add(Directory("src")
             .add(File("main.py", 50))
             .add(File("utils.py", 30))))

print("总大小：", root.accept(SizeCounter()), "KB")
lister = FileLister()
root.accept(lister)
print("文件列表：", lister.paths)
