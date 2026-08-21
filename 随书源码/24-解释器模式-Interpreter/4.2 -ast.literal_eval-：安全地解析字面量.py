# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #6：4.2 `ast.literal_eval`：安全地解析字面量
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# ast.literal_eval：只认字面量，不执行任何代码——安全！
import ast

# 解析配置文件里的"字面量"字符串
print(ast.literal_eval("[1, 2, 3]"))
print(ast.literal_eval("{'name': '小明', 'age': 18}"))
print(ast.literal_eval("(1, 2)"))

# 表达式？不行——literal_eval 只认字面量
try:
    ast.literal_eval("1 + 2")
except ValueError:
    print("拒绝执行表达式：ValueError")
