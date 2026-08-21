# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》13-责任链模式-Chain-of-Responsibility
# 代码块 #6：4.2 装饰器链：Python 原生的"责任链"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def sensitive(func):
    """装饰器 1：敏感词过滤"""
    def wrapper(text):
        text = text.replace("垃圾", "**")
        return func(text)
    return wrapper

def ad_filter(func):
    """装饰器 2：广告标记"""
    def wrapper(text):
        if "加微信" in text:
            text += "（疑似广告）"
        return func(text)
    return wrapper

@sensitive
@ad_filter
def echo(text):
    return text

print(echo("这个垃圾又在加微信卖课"))
