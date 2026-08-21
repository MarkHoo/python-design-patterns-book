# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #2：3.1 经典版：折扣策略（三要素齐全）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class NormalDiscount:
    def discount(self, price: float) -> float:
        return price


class VipDiscount:
    def discount(self, price: float) -> float:
        return price * 0.8


class NewUserDiscount:
    def discount(self, price: float) -> float:
        return price * 0.9


class CheckoutContext:
    """上下文：持有一个策略，负责调用它"""

    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy) -> None:
        """运行时换策略"""
        self._strategy = strategy

    def settle(self, price: float) -> float:
        return self._strategy.discount(price)


cart = CheckoutContext(NormalDiscount())
print("普通用户：", cart.settle(100))

cart.set_strategy(VipDiscount())          # 运行时换算法
print("VIP 用户：", cart.settle(100))

cart.set_strategy(NewUserDiscount())
print("新用户：", cart.settle(100))
