# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #10：误区 4：把责任链当万能，简单 if-elif 就够时硬上链
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 就 3 种固定情况，if-elif 最直白，别上责任链
def grade(score):
    if score >= 90:
        return "优秀"
    elif score >= 60:
        return "及格"
    return "不及格"

for s in (95, 70, 40):
    print(f"{s} 分 → {grade(s)}")
