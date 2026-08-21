# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》04-迭代器模式-Iterator
# 代码块 #14：练习 1：给"扑克牌"实现 `__iter__`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Deck:
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __iter__(self):
        # 答案：列表推导 + iter()，一行搞定
        return iter([f"{r}{s}" for s in self.suits for r in self.ranks])


deck = Deck()
cards = list(deck)
print("总牌数：", len(cards))
print("前 5 张：", cards[:5])
print("后 5 张：", cards[-5:])
