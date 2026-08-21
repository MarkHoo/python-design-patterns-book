# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #9：误区 3：处理顺序依赖
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def add_signature(text):
    return text + " —— 来自系统"

def truncate(text, n=10):
    return text[:n]

msg = "这是一条很长很长的消息内容"
print("A：", truncate(add_signature(msg)))   # 先签名再截断：签名被截掉
print("B：", add_signature(truncate(msg)))   # 先截断再签名：签名保留
