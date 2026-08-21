# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》02-简单工厂-Simple-Factory
# 代码块 #6：4.2 classmethod 工厂：让类自己当工厂
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @classmethod
    def from_dict(cls, data: dict):
        """工厂：从字典创建"""
        return cls(data["name"], data["age"])

    def __repr__(self):
        return f"User({self.name}, {self.age})"


u1 = User("小明", 18)
u2 = User.from_dict({"name": "小红", "age": 20})
print("直接构造：", u1)
print("from_dict 工厂：", u2)
