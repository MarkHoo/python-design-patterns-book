# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #15：练习 2：用 `yield` 重写书架遍历
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class BookShelf:
    def __init__(self, books):
        self._books = books

    def __iter__(self):
        # 答案：yield 版，三行搞定
        for book in self._books:
            yield book


shelf = BookShelf(["三体", "活着", "百年孤独"])
print([f"《{b}》" for b in shelf])
