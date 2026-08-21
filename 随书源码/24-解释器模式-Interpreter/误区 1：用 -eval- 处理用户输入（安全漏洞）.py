# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》24-解释器模式-Interpreter
# 代码块 #9：误区 1：用 `eval` 处理用户输入（安全漏洞）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 误区：eval 用户输入 = 把服务器的钥匙交给陌生人
user_input = "__import__('os').getcwd()"   # 假设这是用户提交的"表达式"

result = eval(user_input)                  # 危险！用户输入被当成代码执行
print("用户输入被执行了，返回类型：", type(result).__name__)
