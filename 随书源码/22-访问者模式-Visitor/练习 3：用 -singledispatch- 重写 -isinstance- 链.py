# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》22-访问者模式-Visitor
# 代码块 #13：练习 3：用 `singledispatch` 重写 `isinstance` 链
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 答案：singledispatch 按类型分派，代替手写 isinstance 链
from functools import singledispatch

@singledispatch
def area(shape):
    raise TypeError(f"不支持的形状：{type(shape).__name__}")

class Circle:
    def __init__(self, r: float):
        self.r = r

class Rect:
    def __init__(self, w: float, h: float):
        self.w = w
        self.h = h

@area.register
def _(shape: Circle) -> float:
    return 3.14 * shape.r ** 2

@area.register
def _(shape: Rect) -> float:
    return shape.w * shape.h

print("圆面积：", round(area(Circle(2)), 2))
print("矩形面积：", area(Rect(3, 4)))
