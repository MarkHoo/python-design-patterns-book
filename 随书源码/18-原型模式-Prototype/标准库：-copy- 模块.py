# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #8：标准库：`copy` 模块
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy

data = [1, 2]
original = [data, data]   # 同一个列表被引用两次

cloned = copy.deepcopy(original)
print("克隆后两个元素仍是同一个对象:", cloned[0] is cloned[1])
print("但与原版已经无关:", cloned[0] is not original[0])
