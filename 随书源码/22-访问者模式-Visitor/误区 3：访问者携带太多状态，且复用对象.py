# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #10：误区 3：访问者携带太多状态，且复用对象
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 误区：访问者对象复用导致状态叠加
class File:
    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_file(self)

class Collector:
    """收集文件名——注意它是有状态的"""

    def __init__(self):
        self.names = []

    def visit_file(self, node: File) -> None:
        self.names.append(node.name)

files = [File("a.txt"), File("b.txt")]
c = Collector()
for f in files:
    f.accept(c)
print("第一次收集：", c.names)

# 同一个访问者再遍历一次，结果叠加了
for f in files:
    f.accept(c)
print("第二次收集：", c.names, "← 重复了！")
