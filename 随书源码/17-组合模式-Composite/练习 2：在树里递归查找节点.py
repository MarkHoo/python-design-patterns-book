# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #13：练习 2：在树里递归查找节点
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：递归查找——先查自己，再查每个孩子
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


def find(node, name: str):
    if node.name == name:
        return node
    for child in node.children:
        result = find(child, name)
        if result is not None:
            return result
    return None


root = Folder("项目")
src = Folder("src")
src.add(File("main.py"))
root.add(src)
root.add(File("README.md"))

target = find(root, "main.py")
print("找到了:", target.name)
print("找不到的返回:", find(root, "不存在.py"))
