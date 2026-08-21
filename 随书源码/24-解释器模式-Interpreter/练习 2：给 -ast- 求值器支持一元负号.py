# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #12：练习 2：给 `ast` 求值器支持一元负号
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：给 ast 求值器加上"一元负号"支持
import ast

class MyEvaluator(ast.NodeVisitor):
    def __init__(self, env: dict):
        self.env = env

    def visit_Constant(self, node):
        return node.value

    def visit_Name(self, node):
        return self.env[node.id]

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            return -operand
        if isinstance(node.op, ast.UAdd):
            return +operand
        raise ValueError("不支持的运算符")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        raise ValueError("不支持的运算符")

ev = MyEvaluator({"x": 5})
print("-x + 3 =", ev.visit(ast.parse("-x + 3", mode="eval").body))
print("--x =", ev.visit(ast.parse("--x", mode="eval").body))
