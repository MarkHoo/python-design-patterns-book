# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #7：4.3 `functools.lru_cache`：标准库自带的享元池
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# functools.lru_cache：标准库自带的"享元工厂"
import functools

@functools.lru_cache(maxsize=None)
def get_glyph(ch: str, font: str) -> tuple:
    print(f"构造字形：{ch!r}/{font}")
    return (ch, font)

g1 = get_glyph("A", "宋体")
g2 = get_glyph("A", "宋体")
g3 = get_glyph("B", "宋体")
print("同参数共享:", g1 is g2)
print("不同参数独立:", g1 is not g3)
