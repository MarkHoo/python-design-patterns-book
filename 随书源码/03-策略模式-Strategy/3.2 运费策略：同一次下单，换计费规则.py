# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #3：3.2 运费策略：同一次下单，换计费规则
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class WeightFee:
    def calculate(self, weight: float, distance: float) -> float:
        return weight * 2.0          # 每公斤 2 元


class DistanceFee:
    def calculate(self, weight: float, distance: float) -> float:
        return distance * 0.5        # 每公里 0.5 元


class FreeFee:
    def calculate(self, weight: float, distance: float) -> float:
        return 0.0                   # 包邮


def show_fee(name: str, fee):
    print(f"{name}：{fee.calculate(weight=5, distance=10)} 元")


show_fee("按重量计费", WeightFee())
show_fee("按距离计费", DistanceFee())
show_fee("全场包邮", FreeFee())
