# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #6：框架：Django 的 QuerySet 链式 API
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class QuerySet:
    """迷你版 Django QuerySet：每个方法返回"新对象"（不可变链式）"""

    def __init__(self, data, filters=None, order=None):
        self._data = data
        self._filters = filters or []
        self._order = order

    def filter(self, predicate):
        """返回新的 QuerySet，原对象不受影响"""
        return QuerySet(self._data, self._filters + [predicate], self._order)

    def order_by(self, key):
        return QuerySet(self._data, self._filters, key)

    def execute(self):
        """相当于真正发 SQL 的那一下"""
        result = self._data
        for f in self._filters:
            result = [x for x in result if f(x)]
        if self._order:
            result = sorted(result, key=self._order)
        return result

products = [
    {"name": "键盘", "price": 199, "stock": 3},
    {"name": "鼠标", "price": 99, "stock": 20},
    {"name": "显示器", "price": 1299, "stock": 5},
]

qs = (QuerySet(products)
      .filter(lambda p: p["stock"] > 0)
      .filter(lambda p: p["price"] < 1000)
      .order_by(lambda p: p["price"]))
for p in qs.execute():
    print(p)
