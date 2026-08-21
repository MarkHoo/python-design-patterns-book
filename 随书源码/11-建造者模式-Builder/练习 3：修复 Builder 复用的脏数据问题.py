# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #12：练习 3：修复 Builder 复用的脏数据问题
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：build 时返回副本并重置内部状态
class SmoothieBuilder:
    """果汁 builder：连续做两杯互不干扰"""

    def __init__(self):
        self.ingredients = []

    def add(self, item):
        self.ingredients.append(item)
        return self

    def build(self):
        result = list(self.ingredients)   # 返回副本，外部改不到内部
        self.ingredients = []             # 重置，下一杯从零开始
        return result

b = SmoothieBuilder()
print("第一杯：", b.add("草莓").add("酸奶").build())
print("第二杯：", b.add("芒果").add("牛奶").build())
