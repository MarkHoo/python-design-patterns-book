# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #13：练习 1：把 if-elif 工厂改写成"字典注册表"版
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Circle:
    def draw(self):
        return "画圆 ⭕"


class Square:
    def draw(self):
        return "画方 ⬜"


SHAPES = {
    "circle": Circle,
    "square": Square,
}


def create_shape(name):
    cls = SHAPES.get(name)
    if cls is None:
        raise ValueError(f"未知形状：{name}")
    return cls()


print(create_shape("circle").draw())
print(create_shape("square").draw())
