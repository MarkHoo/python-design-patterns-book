# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #6：4.2 `ast.NodeVisitor`：标准库内置的"访问者框架"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# ast.NodeVisitor：标准库内置的"访问者框架"
import ast

class FunctionCounter(ast.NodeVisitor):
    """访问者：统计代码里的函数定义数量"""

    def __init__(self):
        self.count = 0

    def visit_FunctionDef(self, node):
        self.count += 1
        self.generic_visit(node)   # 继续往下遍历（函数里还能嵌套函数）

source = """
def greet(name):
    return "你好，" + name

def main():
    def inner(): pass

class Helper:
    def method(self): pass
"""

tree = ast.parse(source)
counter = FunctionCounter()
counter.visit(tree)
print("函数定义数量（含嵌套和类方法）：", counter.count)
