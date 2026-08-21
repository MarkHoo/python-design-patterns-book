# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #11：误区 1：以为可迭代对象就是迭代器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

words = ["a", "b", "c"]
print("list 有 __iter__：", hasattr(words, "__iter__"))
print("list 有 __next__：", hasattr(words, "__next__"))

try:
    next(words)
except TypeError as e:
    print("直接 next(list) 报错：", e)

it = iter(words)                   # 先 iter() 拿到迭代器
print("迭代器有 __next__：", hasattr(it, "__next__"))
print("next(it)：", next(it))
