# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #4：3.3 对比：简单工厂 vs 工厂方法
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

# ===== 简单工厂：加一种动物就要改函数（修改）=====
class Dog:
    def speak(self):
        return "汪汪"


class Cat:
    def speak(self):
        return "喵喵"


def animal_factory_simple(kind: str):
    if kind == "dog":
        return Dog()
    elif kind == "cat":
        return Cat()
    # 加 Duck？改这个函数！——违反开闭原则


# ===== 工厂方法：加一种动物 = 加一对新类（扩展）=====
import abc


class Animal(abc.ABC):
    @abc.abstractmethod
    def speak(self) -> str:
        pass


class Duck(Animal):
    def speak(self) -> str:
        return "嘎嘎"


class AnimalCreator(abc.ABC):
    @abc.abstractmethod
    def create(self) -> Animal:
        pass


class DuckCreator(AnimalCreator):
    def create(self) -> Animal:
        return Duck()   # 新功能 = 新代码，旧代码一行不动


print("简单工厂：", animal_factory_simple("dog").speak())
print("工厂方法：", DuckCreator().create().speak())
