# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》17-组合模式-Composite
# 代码块 #9：误区 1：叶子实现了容器方法，但抛异常
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Node:
    def add(self, child) -> None:
        raise NotImplementedError


class File(Node):
    def __init__(self, name: str):
        self.name = name

    def add(self, child) -> None:
        raise NotImplementedError("文件不能有子节点！")


class Folder(Node):
    def __init__(self):
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)


# 接口统一了，但"文件"被迫实现一个永远用不上的方法
node = File("a.txt")
try:
    node.add(File("b.txt"))
except NotImplementedError as e:
    print("运行时才炸:", e)
