# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》05-装饰器模式-Decorator
# 代码块 #10：4.4 内置装饰器：`@property` / `@staticmethod`
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Circle:
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def area(self) -> float:
        """把方法变成属性：调用时不加括号"""
        return 3.14159 * self._radius ** 2

    @staticmethod
    def describe() -> str:
        """静态方法：不依赖实例"""
        return "我是一个圆"


c = Circle(2.0)
print("面积（当属性用）：", c.area)
print("静态方法：", Circle.describe())
