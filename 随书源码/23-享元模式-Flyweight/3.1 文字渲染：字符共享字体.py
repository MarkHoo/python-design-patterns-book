# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》23-享元模式-Flyweight
# 代码块 #2：3.1 文字渲染：字符共享字体
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 文字渲染：字符+字体是内部状态（共享），位置+颜色是外部状态（每次传）
class Glyph:
    def __init__(self, ch: str, font: str, size: int):
        self.ch = ch
        self.font = font
        self.size = size

    def render(self, x: int, y: int, color: str) -> str:
        return f"{self.ch!r}({self.font},{self.size}) 画在({x},{y}) 颜色{color}"

class GlyphFactory:
    """享元工厂：同一个字符+样式，只创建一个对象"""

    def __init__(self):
        self._pool = {}

    def get(self, ch: str, font: str, size: int) -> Glyph:
        key = (ch, font, size)
        if key not in self._pool:
            self._pool[key] = Glyph(ch, font, size)
        return self._pool[key]

    def size(self) -> int:
        return len(self._pool)

factory = GlyphFactory()
text = "hello"
glyphs = [factory.get(c, "微软雅黑", 12) for c in text]
print(f"创建了 {len(glyphs)} 个引用，但对象只有 {factory.size()} 个")
print("所有 'l' 是同一个对象:", glyphs[2] is glyphs[3])

# 渲染时传入位置和颜色（外部状态）
print(glyphs[0].render(0, 0, "黑色"))
print(glyphs[4].render(10, 0, "红色"))
