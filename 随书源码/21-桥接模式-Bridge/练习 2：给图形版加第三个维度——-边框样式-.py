# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》21-桥接模式-Bridge
# 代码块 #10：练习 2：给图形版加第三个维度——"边框样式"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案思路：边框样式属于"渲染"维度的扩展——给 Renderer 加一个 draw_border 方法
class Renderer:
    def draw_border(self, style: str) -> str:
        return f"绘制{style}边框"


class AsciiRenderer(Renderer):
    def draw_border(self, style: str) -> str:
        return f"ASCII 绘制{style}边框"


class SvgRenderer(Renderer):
    def draw_border(self, style: str) -> str:
        return f"<rect stroke-dasharray={style!r} />"


for r in (AsciiRenderer(), SvgRenderer()):
    print(r.draw_border("虚线"))
