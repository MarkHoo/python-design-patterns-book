# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #2：3.1 经典版：手写迭代协议（书架 + 独立迭代器）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class BookShelf:
    """可迭代对象：书架"""

    def __init__(self, books: list[str]):
        self._books = books

    def __iter__(self):
        return BookIterator(self)   # 每次调用返回一个新的迭代器

    def __len__(self):
        return len(self._books)


class BookIterator:
    """迭代器：记录遍历到哪里了"""

    def __init__(self, shelf: BookShelf):
        self._shelf = shelf
        self._index = 0

    def __next__(self) -> str:
        if self._index >= len(self._shelf):
            raise StopIteration     # 取完了：抛信号告诉 for 结束
        book = self._shelf._books[self._index]
        self._index += 1
        return book


shelf = BookShelf(["三体", "活着", "百年孤独"])
for book in shelf:
    print(f"读到：{book}")
