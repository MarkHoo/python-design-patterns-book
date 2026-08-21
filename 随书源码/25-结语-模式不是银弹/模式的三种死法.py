# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》25-结语-模式不是银弹
# 代码块 #1：模式的三种死法
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：两个分支也要上策略模式 + 抽象工厂 + 单例
from abc import ABC

class DiscountStrategy(ABC): ...      # 就两种折扣，硬造一个策略族
class DiscountFactory: ...            # 又造一个工厂
class DiscountRegistry: ...           # 再来个注册表


# 正道：两个分支，一个函数搞定
def discount(price: float, is_vip: bool) -> float:
    return price * 0.8 if is_vip else price * 0.95


print("普通用户：", discount(100, False))
print("VIP 用户：", discount(100, True))
