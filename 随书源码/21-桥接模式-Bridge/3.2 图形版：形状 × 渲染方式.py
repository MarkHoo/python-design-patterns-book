# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》21-桥接模式-Bridge
# 代码块 #3：3.2 图形版：形状 × 渲染方式
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Renderer:
    """实现维度：渲染引擎"""

    def draw_line(self, x1, y1, x2, y2) -> str: ...
    def draw_circle(self, cx, cy, r) -> str: ...


class AsciiRenderer(Renderer):
    """字符画渲染"""

    def draw_line(self, x1, y1, x2, y2) -> str:
        return f"ASCII 画线 ({x1},{y1})-({x2},{y2})"

    def draw_circle(self, cx, cy, r) -> str:
        return f"ASCII 画圆 圆心({cx},{cy}) 半径{r}"


class SvgRenderer(Renderer):
    """矢量渲染"""

    def draw_line(self, x1, y1, x2, y2) -> str:
        return f"<line x1={x1} y1={y1} x2={x2} y2={y2} />"

    def draw_circle(self, cx, cy, r) -> str:
        return f"<circle cx={cx} cy={cy} r={r} />"


class Shape:
    """抽象维度：形状"""

    def __init__(self, renderer: Renderer):
        self._renderer = renderer

    def render(self) -> None: ...


class Line(Shape):
    def __init__(self, renderer: Renderer, x1, y1, x2, y2):
        super().__init__(renderer)
        self._points = (x1, y1, x2, y2)

    def render(self) -> None:
        print(self._renderer.draw_line(*self._points))


class Circle(Shape):
    def __init__(self, renderer: Renderer, cx, cy, r):
        super().__init__(renderer)
        self._circle = (cx, cy, r)

    def render(self) -> None:
        print(self._renderer.draw_circle(*self._circle))


# 2 种形状 × 2 种渲染 = 4 种组合，只有 4 个类（没有桥接要 4 个类，但加维度就爆炸）
for shape in (Line(AsciiRenderer(), 0, 0, 10, 10),
              Circle(AsciiRenderer(), 5, 5, 3),
              Line(SvgRenderer(), 0, 0, 10, 10),
              Circle(SvgRenderer(), 5, 5, 3)):
    shape.render()
