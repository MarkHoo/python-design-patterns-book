# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #14：练习 3：用"字典注册策略表"实现会员积分
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def points_normal(amount: float) -> int:
    return int(amount)          # 1 元 1 分


def points_double(amount: float) -> int:
    return int(amount) * 2      # 双倍积分日


def points_birthday(amount: float) -> int:
    return int(amount) * 3      # 生日三倍


POINTS_RULES = {
    "normal": points_normal,
    "double": points_double,
    "birthday": points_birthday,
}


def earn_points(amount: float, rule: str) -> int:
    return POINTS_RULES[rule](amount)


print("普通日购物 100 元：", earn_points(100, "normal"), "分")
print("双倍日购物 100 元：", earn_points(100, "double"), "分")
print("生日购物 100 元：", earn_points(100, "birthday"), "分")
