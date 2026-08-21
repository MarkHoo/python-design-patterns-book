# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #6：4.2 实现 `__iter__` / `__len__`：组合直接支持遍历
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class File:
    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return ()

    def __iter__(self):
        return iter(())        # 叶子迭代 = 空

    def __len__(self):
        return 0


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def __iter__(self):
        return iter(self.children)     # 迭代 = 遍历直接子节点

    def __len__(self):
        return len(self.children)


root = Folder("工作")
docs = Folder("文档")
docs.add(File("需求.md"))
docs.add(File("设计.md"))
root.add(docs)
root.add(File("README.txt"))

print("工作目录下条目数:", len(root))
print("文档目录下条目数:", len(docs))
for node in root:
    print("直接子节点:", node.name)
