# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #9：`zip` / `enumerate` / `map`：全是惰性迭代器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

names = ["小明", "小红", "小刚"]
scores = [88, 95, 72]

pairs = zip(names, scores)         # zip 是迭代器，用一次就没了
print("zip 配对：", list(pairs))

print("enumerate 带下标：", list(enumerate(names)))

print("map 映射：", list(map(str.upper, ["a", "b", "c"])))

info = {"name": "小明", "age": 18}
print("dict 默认遍历键：", list(info))
print("dict.items() 遍历键值：", list(info.items()))
