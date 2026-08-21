# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #11：练习 2：写一个搜索条件构造器
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：
class SearchBuilder:
    def __init__(self):
        self._cond = {"keyword": "", "category": None, "min_price": None, "max_price": None}

    def keyword(self, kw):
        self._cond["keyword"] = kw
        return self

    def category(self, c):
        self._cond["category"] = c
        return self

    def price_range(self, low, high):
        self._cond["min_price"] = low
        self._cond["max_price"] = high
        return self

    def build(self):
        return dict(self._cond)     # 返回副本，防止外部改到内部

cond = (SearchBuilder()
        .keyword("机械键盘")
        .category("外设")
        .price_range(100, 500)
        .build())
print(cond)
