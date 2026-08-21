# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》03-策略模式-Strategy
# 代码块 #4：3.3 排序策略：同一个商品列表，换算法就换顺序
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class PriceAsc:
    def sort(self, items: list):
        return sorted(items, key=lambda p: p["price"])


class PriceDesc:
    def sort(self, items: list):
        return sorted(items, key=lambda p: p["price"], reverse=True)


class RatingDesc:
    def sort(self, items: list):
        return sorted(items, key=lambda p: p["rating"], reverse=True)


def show(name: str, items: list):
    print(name + "：", [p["name"] for p in items])


products = [
    {"name": "键盘", "price": 199, "rating": 4.5},
    {"name": "鼠标", "price": 89, "rating": 4.8},
    {"name": "显示器", "price": 1299, "rating": 4.2},
]

show("价格从低到高", PriceAsc().sort(products))
show("价格从高到低", PriceDesc().sort(products))
show("评分从高到低", RatingDesc().sort(products))
