# -*- coding: utf-8 -*-
# 来源：《Python 设计模式修炼手册》07-工厂方法-Factory-Method
# 代码块 #9：误区 1：把工厂方法当成"换了个名字的简单工厂"
# 本书承诺：本文件与书中代码逐字一致，可独立运行。

class ConsoleLogger:
    def log(self, m):
        print(f"[控制台] {m}")


class FileLogger:
    def log(self, m):
        print(f"[文件] {m}")


class FakeFactory:
    """反面教材：抽象工厂里写 if-elif——本质还是简单工厂"""
    def create_logger(self, kind):
        if kind == "console":
            return ConsoleLogger()
        elif kind == "file":
            return FileLogger()
        raise ValueError(kind)


FakeFactory().create_logger("console").log("你好")
