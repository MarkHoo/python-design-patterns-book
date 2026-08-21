# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #11：练习 1：用 `ast.NodeVisitor` 统计赋值语句
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：继承 NodeVisitor，重写 visit_Assign
import ast

class AssignCounter(ast.NodeVisitor):
    def __init__(self):
        self.count = 0

    def visit_Assign(self, node):
        self.count += 1
        self.generic_visit(node)

source = """
x = 1
y = x + 2
z = y * 3
"""

counter = AssignCounter()
counter.visit(ast.parse(source))
print("赋值语句数量：", counter.count)
