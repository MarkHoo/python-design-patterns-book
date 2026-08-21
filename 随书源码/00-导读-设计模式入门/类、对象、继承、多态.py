# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》00-导读-设计模式入门
# 代码块 #1：类、对象、继承、多态
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Animal:
    """所有动物的基类"""

    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "..."


class Dog(Animal):
    def speak(self) -> str:
        return "汪汪！"


class Cat(Animal):
    def speak(self) -> str:
        return "喵～"


def let_it_talk(animal: Animal) -> None:
    """多态：不管传入什么动物，都能让它开口"""
    print(f"{animal.name}说：{animal.speak()}")


let_it_talk(Dog("旺财"))
let_it_talk(Cat("咪咪"))
let_it_talk(Animal("无名氏"))
