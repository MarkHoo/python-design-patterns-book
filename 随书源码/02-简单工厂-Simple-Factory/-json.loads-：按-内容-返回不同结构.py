# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #9：`json.loads`：按"内容"返回不同结构
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import json

result_a = json.loads('{"name": "小明"}')   # 内容是对象 → dict
result_b = json.loads('[1, 2, 3]')          # 内容是数组 → list
result_c = json.loads('"hello"')            # 内容是字符串 → str

print("类型 1：", type(result_a).__name__, result_a)
print("类型 2：", type(result_b).__name__, result_b)
print("类型 3：", type(result_c).__name__, result_c)
