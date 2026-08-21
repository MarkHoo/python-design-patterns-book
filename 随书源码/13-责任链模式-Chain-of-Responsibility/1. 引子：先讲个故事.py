# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：报销审批用 if-elif 硬编码，加一级审批就要改函数
def approve(amount):
    if amount <= 500:
        return "组长审批通过"
    elif amount <= 5000:
        return "经理审批通过"
    elif amount <= 50000:
        return "总监审批通过"
    else:
        return "需要董事会审批"

print(approve(300))
print(approve(3000))
print(approve(30000))
print(approve(300000))
