# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #13：误区 3：遍历的时候修改集合
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

data = {"a": 1, "b": 2, "c": 3}
try:
    for key in data:
        if key == "b":
            data.pop(key)
except RuntimeError as e:
    print("报错：", e)
