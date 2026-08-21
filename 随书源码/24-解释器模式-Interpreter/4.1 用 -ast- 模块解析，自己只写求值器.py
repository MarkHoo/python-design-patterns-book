# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #5：4.1 用 `ast` 模块解析，自己只写求值器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 用标准库 ast 做语法分析，自己只写求值器
import ast

class MyEvaluator(ast.NodeVisitor):
    """遍历 ast 生成的表达式树并求值（支持变量）"""

    def __init__(self, env: dict):
        self.env = env

    def visit_Constant(self, node):
        return node.value

    def visit_Name(self, node):
        if node.id not in self.env:
            raise NameError(f"未定义变量：{node.id}")
        return self.env[node.id]

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        raise ValueError(f"不支持的运算：{type(node.op).__name__}")

tree = ast.parse("price * qty - 10", mode="eval")
ev = MyEvaluator({"price": 30, "qty": 2})
print("price * qty - 10 =", ev.visit(tree.body))
