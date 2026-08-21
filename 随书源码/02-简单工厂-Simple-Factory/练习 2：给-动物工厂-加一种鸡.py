# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #14：练习 2：给"动物工厂"加一种鸡
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Dog:
    def speak(self):
        return "汪汪！"


class Cat:
    def speak(self):
        return "喵～"


class Chicken:
    def speak(self):
        return "咯咯咯！"


def create_animal(kind):
    if kind == "dog":
        return Dog()
    elif kind == "cat":
        return Cat()
    elif kind == "chicken":
        return Chicken()
    else:
        raise ValueError(f"没有这种动物：{kind}")


for kind in ["dog", "cat", "chicken"]:
    print(f"{kind}：{create_animal(kind).speak()}")
