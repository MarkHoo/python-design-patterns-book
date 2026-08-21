# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #6：4.2 字典注册策略表：一个 dict 装下所有算法
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def fee_wechat(amount: float) -> float:
    return amount * 0.006   # 微信费率 0.6%


def fee_alipay(amount: float) -> float:
    return amount * 0.006


def fee_unionpay(amount: float) -> float:
    return amount * 0.008


FEE_STRATEGIES = {
    "wechat": fee_wechat,
    "alipay": fee_alipay,
    "unionpay": fee_unionpay,
}


def pay(amount: float, channel: str) -> float:
    """上下文：查表拿到算法并执行"""
    return amount + FEE_STRATEGIES[channel](amount)


for ch in FEE_STRATEGIES:
    print(f"{ch} 付 1000 元，实付 {pay(1000, ch):.2f}")
