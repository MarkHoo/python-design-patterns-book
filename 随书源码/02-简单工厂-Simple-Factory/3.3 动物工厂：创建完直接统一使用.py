# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #4：3.3 动物工厂：创建完直接统一使用
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class Dog:
    def speak(self) -> str:
        return "汪汪！"


class Cat:
    def speak(self) -> str:
        return "喵～"


class Duck:
    def speak(self) -> str:
        return "嘎嘎！"


def create_animal(kind: str):
    """动物工厂：报个种类，返回对应的动物"""
    if kind == "dog":
        return Dog()
    elif kind == "cat":
        return Cat()
    elif kind == "duck":
        return Duck()
    else:
        raise ValueError(f"没有这种动物：{kind}")


for kind in ["dog", "cat", "duck"]:
    print(f"{kind}：{create_animal(kind).speak()}")
