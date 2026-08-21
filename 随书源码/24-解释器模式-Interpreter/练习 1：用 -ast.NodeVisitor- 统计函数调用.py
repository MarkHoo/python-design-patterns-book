# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #11：练习 1：用 `ast.NodeVisitor` 统计函数调用
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：统计代码里所有函数调用
import ast


class CallCounter(ast.NodeVisitor):
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        self.generic_visit(node)


source = "print(len('abc')) + str(42)"
counter = CallCounter()
counter.visit(ast.parse(source))
print("函数调用：", counter.calls)
