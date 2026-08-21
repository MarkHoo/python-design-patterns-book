# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #8：5.2 `ast` 模块：Python 自己也在用解释器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# ast：Python 官方用 ast 模块来"读懂"你的源码
import ast

source = """
def add(a, b):
    return a + b
"""
tree = ast.parse(source)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        print("找到函数：", node.name, "参数：", [a.arg for a in node.args.args])
