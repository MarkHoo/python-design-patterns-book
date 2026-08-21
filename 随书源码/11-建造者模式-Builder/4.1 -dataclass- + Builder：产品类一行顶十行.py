# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》11-建造者模式-Builder
# 代码块 #5：4.1 `dataclass` + Builder：产品类一行顶十行
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

from dataclasses import dataclass, field

@dataclass
class Query:
    """产品：数据库查询。dataclass 自动生成 __init__ 和 __repr__"""
    table: str
    columns: list[str] = field(default_factory=list)
    where: str = ""
    order_by: str = ""
    limit: int = 0

class QueryBuilder:
    def __init__(self, table):
        self._q = Query(table=table)

    def select(self, *cols):
        self._q.columns.extend(cols)
        return self

    def filter(self, condition):
        self._q.where = condition
        return self

    def sort(self, col):
        self._q.order_by = col
        return self

    def take(self, n):
        self._q.limit = n
        return self

    def build(self):
        return self._q

q = (QueryBuilder("orders")
     .select("id", "amount")
     .filter("amount > 100")
     .sort("created_at")
     .take(50)
     .build())
print(q)
print("生成的 SQL：", f"SELECT {', '.join(q.columns)} FROM {q.table} WHERE {q.where} ORDER BY {q.order_by} LIMIT {q.limit}")
