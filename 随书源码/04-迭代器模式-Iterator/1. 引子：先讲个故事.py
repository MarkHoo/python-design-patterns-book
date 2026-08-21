# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有迭代协议的世界——自己写的集合没法用 for 遍历
class BookShelf:
    def __init__(self):
        self._books = ["三体", "活着", "百年孤独"]

    def count(self):
        return len(self._books)

    def get(self, index):
        return self._books[index]


shelf = BookShelf()
try:
    for book in shelf:
        print(book)
except TypeError as e:
    print("报错：", e)
