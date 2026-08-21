# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》18-原型模式-Prototype
# 代码块 #11：误区 3：以为原型能解决一切复制问题
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

import copy

# 循环引用：A 引用 B，B 又引用 A——deepcopy 能优雅处理
class Node:
    def __init__(self, name):
        self.name = name
        self.friend = None


a = Node("阿伟")
b = Node("小明")
a.friend = b
b.friend = a

a2 = copy.deepcopy(a)
print("克隆体内部引用也成环:", a2.friend.friend is a2)
print("与原版完全无关:", a2 is not a and a2.friend is not b)
