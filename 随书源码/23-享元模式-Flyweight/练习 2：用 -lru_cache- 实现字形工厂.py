# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #13：练习 2：用 `lru_cache` 实现字形工厂
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：用 lru_cache 实现字形工厂（一行搞定缓存）
import functools

@functools.lru_cache(maxsize=None)
def get_glyph(ch: str, font: str, size: int) -> tuple:
    return (ch, font, size)

text = "abracadabra"
glyphs = [get_glyph(c, "黑体", 14) for c in text]
print("字符数：", len(glyphs), "，共享字形数：", get_glyph.cache_info().currsize)
print("两个 'a' 是同一份:", get_glyph("a", "黑体", 14) is get_glyph("a", "黑体", 14))
