# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #5：4.1 `classmethod` 作为工厂方法：类方法多态
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Animal:
    """产品基类：同时充当自己的工厂"""

    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "……"

    @classmethod
    def from_line(cls, line: str):
        """工厂方法：从一行文本创建实例。
        关键在 cls——子类调用时，cls 自动是子类自己！"""
        name = line.strip().split(":")[0]
        return cls(name)


class Dog(Animal):
    def speak(self) -> str:
        return "汪汪"


class Cat(Animal):
    def speak(self) -> str:
        return "喵喵"


# 同一个工厂方法，子类调用自动返回子类实例——"类方法多态"
for animal in [Dog.from_line("旺财"), Cat.from_line("咪咪")]:
    print(f"{animal.name}说：{animal.speak()}")
