# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》00-导读-设计模式入门
# 代码块 #2：鸭子类型：Python 的多态更狂野
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

def let_it_talk(animal) -> None:
    """只要对象有 speak 方法，就能让它开口（鸭子类型）"""
    print(f"{animal.name}说：{animal.speak()}")


class Robot:
    """机器人不是 Animal 的子类，但它有 speak 方法"""

    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "哔哔——电池电量 99%"


let_it_talk(Robot("R2-D2"))  # 照样能说话！
