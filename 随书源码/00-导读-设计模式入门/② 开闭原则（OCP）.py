# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》00-导读-设计模式入门
# 代码块 #5：② 开闭原则（OCP）
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# 反面教材：每加一种形状，就要改一次 draw_all
def draw_all_v1(shapes: list) -> None:
    for s in shapes:
        if s["type"] == "circle":
            print("画圆")
        elif s["type"] == "square":
            print("画方")
        # 加三角形？改这里！


# 正确姿势：让每种形状自己会画，新增形状不用动旧代码
class Shape:
    def draw(self) -> None: ...


class Circle(Shape):
    def draw(self) -> None:
        print("画一个圆 ⭕")


class Square(Shape):
    def draw(self) -> None:
        print("画一个方 ⬜")


class Triangle(Shape):  # 新形状 = 新类，旧代码一行不用改
    def draw(self) -> None:
        print("画一个三角 🔺")


def draw_all(shapes: list[Shape]) -> None:
    for s in shapes:
        s.draw()


draw_all([Circle(), Square(), Triangle()])
