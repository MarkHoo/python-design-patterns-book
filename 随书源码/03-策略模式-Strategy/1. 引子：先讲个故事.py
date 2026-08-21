# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有策略的世界——折扣逻辑全堆在结账函数里
def checkout(price: float, user_type: str) -> float:
    """结账：按用户类型算折扣"""
    if user_type == "vip":
        return price * 0.8
    elif user_type == "svip":
        return price * 0.7
    elif user_type == "new_user":
        return price * 0.9
    else:
        return price


print("普通用户：", checkout(100, "normal"))
print("VIP 用户：", checkout(100, "vip"))
print("SVIP 用户：", checkout(100, "svip"))
