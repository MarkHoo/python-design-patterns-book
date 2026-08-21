# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #8：`sorted(key=...)`：内置的"策略注入点"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

students = [
    {"name": "小明", "score": 88},
    {"name": "小红", "score": 95},
    {"name": "小刚", "score": 72},
]

by_name = sorted(students, key=lambda s: s["name"])
by_score = sorted(students, key=lambda s: s["score"])
by_score_desc = sorted(students, key=lambda s: s["score"], reverse=True)

print("按名字排：", [s["name"] for s in by_name])
print("按分数排：", [s["name"] for s in by_score])
print("按分数倒序：", [s["name"] for s in by_score_desc])
print("最高分：", max(students, key=lambda s: s["score"])["name"])
print("最低分：", min(students, key=lambda s: s["score"])["name"])
