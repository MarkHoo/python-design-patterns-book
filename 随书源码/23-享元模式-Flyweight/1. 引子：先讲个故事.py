# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #1：1. 引子：先讲个故事
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 引子：没有享元的世界——每个字符都自带一套完整样式
class Character:
    def __init__(self, ch: str, font: str, size: int, color: str):
        self.ch = ch
        self.font = font
        self.size = size
        self.color = color

text = "hello" * 2000      # 一页文章：1 万个字符
chars = [Character(c, "微软雅黑", 12, "#333333") for c in text]

unique = len({c.ch for c in chars})
print(f"共创建 {len(chars)} 个字符对象")
print(f"其中不同的字符只有 {unique} 种")
print("字体、字号、颜色被重复存了", len(chars), "份")
