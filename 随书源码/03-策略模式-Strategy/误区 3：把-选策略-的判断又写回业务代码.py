# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #11：误区 3：把"选策略"的判断又写回业务代码
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 误区 3：选择策略的判断又写回业务代码——if-elif 只是搬了家
def settle_bad(price: float, user_type: str) -> float:
    if user_type == "vip":
        return price * 0.8
    elif user_type == "new":
        return price * 0.9
    return price


# 正确姿势：策略表收拢选择逻辑，业务代码只认策略名
STRATEGIES = {
    "vip": lambda p: p * 0.8,
    "new": lambda p: p * 0.9,
    "normal": lambda p: p,
}


def settle(price: float, user_type: str) -> float:
    return STRATEGIES[user_type](price)


print("坏味道：", settle_bad(100, "vip"))
print("正确姿势：", settle(100, "vip"))
